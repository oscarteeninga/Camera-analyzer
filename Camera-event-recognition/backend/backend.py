import threading
import time

from config.cameraconfig import CameraConfig
from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_restplus import Api, fields, Resource
from model.analyzer import CameraAnalyzer
from services.areaservice import AreaService
from services.cacheservice import cache, Dictionaries
from services.cameraservice import CameraService
from services.eventservice import EventService

receivers = {}
event_service = EventService()
area_service = AreaService()
camera_service = CameraService()

flask_app = Flask(__name__)
CORS(flask_app)
app = Api(app=flask_app, title="Camera Api", default="Camera Api", default_label="Camera Api")

cache.init_app(flask_app)
ip_to_name, name_to_ip = camera_service.get_camera_name_id_mapping()
cache.add(Dictionaries.CAMERA_IP_TO_NAME, ip_to_name)
cache.add(Dictionaries.CAMERA_NAME_TO_IP, name_to_ip)
cache.add(Dictionaries.AREAS, area_service.get_areas())

configuration_name_space = app.namespace('Configuration', description='Cameras configuration')
camera_post = app.model('Camera configuration params', {
    'ip': fields.String(required=True, description='Camera ip address'),
    'name': fields.String(required=True, description='Name of the camera'),
    'user': fields.String(required=True, description='Camera user'),
    'password': fields.String(required=True, description='Password to camera')
})

camera_update = app.model('Camera configuration params', {
    'ip': fields.String(required=True, description='Camera ip address'),
    'name': fields.String(required=True, description='Name of the camera'),
    'user': fields.String(required=True, description='Camera user'),
    'password': fields.String(required=True, description='Password to camera'),
    'id': fields.String(required=True, description='Camera id')
})

area = app.model('Area configuration params', {
    'area_name': fields.String(required=True, description='Name of area'),
    'area_confidence_required': fields.Float(required=True,
                                             description='surface of object needed to be assign to area?'),
    'area_x': fields.Float(required=True, description='X cord of start of area'),
    'area_y': fields.Float(required=True, description='Y cord of start of area'),
    'area_width': fields.Float(required=True,
                               description='The width of area'),
    'area_height': fields.Float(required=True, description='The height of area')
})


@app.route("/timestamp")
class Events(Resource):
    @app.doc(params={'date_from': 'Oldest date from which events are downloaded'})
    def get(self):
        return str(time.time() * 1000)


@app.route("/events")
class Events(Resource):
    @app.doc(params={'date_from': 'Oldest date from which events are downloaded'})
    @app.doc(params={'page': 'Oldest date from which events are downloaded'})
    @app.doc(params={'size': 'Oldest date from which events are downloaded'})
    def get(self):
        """Return list of events at a given time"""
        date_from = request.args.get("date_from")
        pagearg = request.args.get("page")
        if pagearg is not None:
            page = int(pagearg)
        else:
            page = None
        sizearg = request.args.get("size")
        if sizearg is not None:
            size = int(sizearg)
        else:
            size = None
        events = event_service.get_events(page, size, date_from)
        print("Returned " + str(len(events)) + " events")
        return events


@app.route('/devices')
class Devices(Resource):
    def get(self):
        """Returns list of devices"""
        response = jsonify(camera_service.get_cameras())
        response.headers.add('Access-Control-Allow-Origin', '*')
        return response

    def post(self):
        """Create configuration of camera"""
        name = request.json['name']
        ip = request.json['ip']
        username = request.json['user']
        password = request.json['password']
        id = camera_service.add_config(CameraConfig(name, ip, username, password))
        response = jsonify(camera_service.get_camera(id))
        return response


@app.route('/devices/<id>')
class DevicesSingle(Resource):
    def get(self, id):
        """Returns list of devices"""
        response = jsonify(camera_service.get_cameras())
        return response

    def put(self, id):
        name = request.json['name']
        ip = request.json['ip']
        username = request.json['user']
        password = request.json['password']
        id = camera_service.update_config(id, name, ip, username, password)
        response = jsonify(camera_service.get_camera(id))
        return response

    def delete(self, id):
        camera_service.delete_config(id)


@app.route('/device/<id>/areas')
class DeviceAreas(Resource):
    def get(self, id):
        """Return list of areas for device of given id"""
        return area_service.get_areas(id=id)

    @app.expect(area)
    def post(self, id):
        """Add new area to device of given id"""
        name = request.json['area_name']
        confidence_required = request.json['area_confidence_required']
        x = request.json['area_x']
        y = request.json['area_y']
        w = request.json['area_width']
        h = request.json['area_height']
        area_service.add_area(name, confidence_required, x, y, w, h, id)
        return {'success': True}, 200, {'ContentType': 'application/json'}


@app.route('/device/<id>/area/<name>')
class DeviceArea(Resource):
    def get(self, id, name):
        """Return list of areas for device of given id"""
        return area_service.get_areas(id=id, name=name)

    @app.expect(area)
    def put(self, id, name):
        """Add new area to device of given id"""
        new_name = request.json['area_name']
        confidence_required = request.json['area_confidence_required']
        x = request.json['area_x']
        y = request.json['area_y']
        w = request.json['area_width']
        h = request.json['area_height']
        area_service.update_area(new_name, confidence_required, x, y, w, h, id, name)
        return {'success': True}, 200, {'ContentType': 'application/json'}

    def delete(self, id, name):
        area_service.delete_area(id, name)
        return {'success': True}, 200, {'ContentType': 'application/json'}


@app.route('/state')
class States(Resource):
    def get(self):
        """"Get states of all cameras"""
        states = {}
        for conf in camera_service.get_configs():
            states[conf.name] = "on" if receivers.get(conf.name) else "off"
        return jsonify(states)


@app.route("/state/<string:camera_name>")
class State(Resource):
    @app.doc(params={'camera_id': 'Id of camera which state will be returned'})
    def get(self, camera_name):
        """Get state of camera with given id"""
        conf = camera_service.get_config(camera_name)
        if conf is None:
            return "Camera does not exists", 404
        elif conf in receivers.keys():
            return jsonify("on")
        else:
            return jsonify("off")


@app.route("/on")
class StartAll(Resource):
    def post(self):
        """Start all cameras registered in the system"""
        for conf in camera_service.get_configs():
            camera_analyzer = CameraAnalyzer(conf)
            thread = threading.Thread(target=camera_analyzer.video, args=(True,))
            thread.start()
            receivers[conf.name] = camera_analyzer
        return {'success': True}, 200, {'ContentType': 'application/json'}


@app.route('/on/<camera_id>')
class startSingleCamera(Resource):
    @app.doc(params={'camera_id': 'Id of camera which will be started'})
    def post(self, camera_id):
        """Start camera with given id"""
        conf = camera_service.get_config(camera_id)
        if conf is None:
            return "Receiver not found", 404
        elif conf in receivers.keys():
            return "Analyzer already started"
        else:
            camera_analyzer = CameraAnalyzer(conf)
            thread = threading.Thread(target=camera_analyzer.video, args=(True,))
            thread.start()
            receivers[conf] = camera_analyzer
            return "Analyzer " + camera_id + " started!"


@app.route('/off/<camera_name>')
class stopSingleCamera(Resource):
    @app.doc(params={'camera_name': 'Name of camera which will be stopped'})
    def post(self, camera_name):
        """Stop camera with given id"""
        conf = camera_service.get_config(camera_name)
        if conf is None:
            return "Receiver not found"
        elif conf not in receivers.keys():
            return "Analyzer already stopped"
        else:
            receivers[conf].terminate()
            receivers.pop(conf)
            return "Analyzer " + camera_name + " stopped"


@app.route('/off')
class StopCamera(Resource):
    def post(self):
        """Stop all cameras"""
        for receiver in receivers:
            receiver.stop()
        receivers.clear()


@configuration_name_space.route("/")
class CameraConfiguration(Resource):
    @app.expect(camera_post)
    def post(self):
        """Create configuration of camera"""
        name = request.json['name']
        ip = request.json['ip']
        username = request.json['user']
        password = request.json['password']
        camera_service.add_config(CameraConfig(name, ip, username, password))

    @app.doc(params={'name': 'Name of camera'})
    def get(self):
        """Get configuration of camera"""
        name = request.args.get("name")
        if name:
            return camera_service.get_config(name).serialize()
        else:
            return "No name given"

    @app.expect(camera_update)
    def put(self, id):
        name = request.json['name']
        ip = request.json['ip']
        username = request.json['user']
        password = request.json['password']
        camera_service.update_config(id, name, ip, username, password)


@configuration_name_space.route('/all')
class CameraConfigurations(Resource):
    def get(self):
        """Get all configurations of cameras"""
        return [config.serialize() for config in camera_service.get_configs()]


@configuration_name_space.route('/areas')
class Area(Resource):
    def get(self):
        """Get all area"""
        return jsonify(cache.get(Dictionaries.AREAS))
