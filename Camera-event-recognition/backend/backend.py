import threading
import time

from flask import Flask, request, jsonify
from flask_restplus import Api, fields, Resource

from config.cameraconfig import CameraConfig
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
app = Api(app=flask_app, title="Camera Api", default="Camera Api", default_label="Camera Api")

cache.init_app(flask_app)
ip_to_name, name_to_ip = camera_service.get_camera_name_id_mapping()
cache.add(Dictionaries.CAMERA_IP_TO_NAME, ip_to_name)
cache.add(Dictionaries.CAMERA_NAME_TO_IP, name_to_ip)
cache.add(Dictionaries.AREAS, area_service.get_areas())

configuration_name_space = app.namespace('Configuration', description='Cameras configuration')
camera_post = app.model('Camera configuration params', {
    'camera_ip': fields.String(required=True, description='Camera ip address'),
    'camera_name': fields.String(required=True, description='Name of the camera'),
    'camera_user': fields.String(required=True, description='Camera user'),
    'camera_password': fields.String(required=True, description='Password to camera'),
    'camera_fps': fields.Integer(required=True,
                                 description='Frames per second that camera will run'),
})

camera_update = app.model('Camera configuration params', {
    'camera_ip': fields.String(required=True, description='Camera ip address'),
    'camera_name': fields.String(required=True, description='Name of the camera'),
    'camera_user': fields.String(required=True, description='Camera user'),
    'camera_password': fields.String(required=True, description='Password to camera'),
    'camera_fps': fields.Integer(required=True,
                                 description='Frames per second that camera will run'),
    'camera_id': fields.String(required=True, description='Camera id')
})

area_post = app.model('Area configuration params', {
    'area_name': fields.String(required=True, description='Name of area'),
    'area_confidence_required': fields.Float(required=True,
                                             description='surface of object needed to be assign to area?'),
    'area_x': fields.Float(required=True, description='X cord of start of area'),
    'area_y': fields.Float(required=True, description='Y cord of start of area'),
    'area_width': fields.Float(required=True,
                               description='The width of area'),
    'area_height': fields.Float(required=True, description='The height of area'),
    'camera_name': fields.String(required=True, description='Name of camera which we want add area to')
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
    @app.doc(params={'camera_id': 'Id of camera which will be stopped'})
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
        name = request.json['camera_name']
        ip = request.json['camera_ip']
        username = request.json['camera_user']
        password = request.json['camera_password']
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
    def put(self):
        id = request.json['camera_id']
        name = request.json['camera_name']
        ip = request.json['camera_ip']
        username = request.json['camera_user']
        password = request.json['camera_password']
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

    @app.expect(area_post)
    def post(self):
        """Add new area"""
        name = request.json['area_name']
        confidence_required = request.json['area_confidence_required']
        x = request.json['area_x']
        y = request.json['area_y']
        w = request.json['area_width']
        h = request.json['area_height']
        camera_name = request.json['camera_name']
        area_service.add_area(name, confidence_required, x, y, w, h, camera_name)
