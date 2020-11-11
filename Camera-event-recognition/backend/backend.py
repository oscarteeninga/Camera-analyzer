import threading

from flask import Flask, request, jsonify
from flask_restplus import Api, fields, Resource

from config.cameraconfig import CameraConfig
from model.receiver import CameraAnalyzer
from services.areaservice import AreaService
from services.cameraservice import CameraService
from services.eventservice import EventService

receivers = {}

flask_app = Flask(__name__)
app = Api(app=flask_app, title="Camera Api", default="Camera Api", default_label="Camera Api")
event_service = EventService()
area_service = AreaService()
camera_service = CameraService()
configuration_name_space = app.namespace('Configuration', description='Cameras configuration')
camera_post = app.model('Camera configuration params', {
    'camera_ip': fields.String(required=True, description='Camera ip address'),
    'camera_name': fields.String(required=True, description='Name of the camera'),
    'camera_user': fields.String(required=True, description='Camera user'),
    'camera_password': fields.String(required=True, description='Password to camera'),
    'camera_fps': fields.Integer(required=True, description='Frames per second that camera will run'),
})


@app.route("/events")
class Events(Resource):
    @app.doc(params={'date_from': 'Oldest date from which events are downloaded'})
    def get(self):
        """Return list of events at a given time"""
        date_from = request.args.get("date_from")
        return event_service.get_events(date_from)


@app.route('/devices')
class Devices(Resource):
    def get(self):
        """Returns list of devices"""
        return jsonify(list(camera_service.get_names()))


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
        conf = camera_service.get_config(camera_name, api=True)
        if conf is None:
            return "Camera does not exists", 404
        elif conf in receivers.keys():
            return jsonify("on")
        else:
            return jsonify("off")


@app.route("/start")
class StartAll(Resource):
    def post(self):
        """Start all cameras registered in the system"""
        for conf in camera_service.get_configs():
            camera_analyzer = CameraAnalyzer(conf)
            thread = threading.Thread(target=camera_analyzer.video, args=(True, True,))
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
            thread = threading.Thread(target=camera_analyzer.video, args=(True, True,))
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
        fps = int(request.json['camera_fps'])
        camera_service.add_config(CameraConfig(name, ip, username, password, fps))

    @app.doc(params={'id': 'Id of camera which the configuration is returned'})
    def get(self):
        """Get configuration of camera"""
        name = request.args.get("name")
        if name:
            return camera_service.get_config(name, api=True).serialize()
        else:
            return "No name given"


@configuration_name_space.route('/all')
class CameraConfigurations(Resource):
    def get(self):
        """Get all configurations of cameras"""
        return [config.serialize() for config in camera_service.get_configs()]


@configuration_name_space.route('/areas')
class Area(Resource):
    def get(self):
        """Get all area"""
        return jsonify(area_service.get_areas())
