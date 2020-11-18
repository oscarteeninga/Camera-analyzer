import threading
import time
import numpy as np
import io
from PIL import Image

from config.cameraconfig import CameraConfig
from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
from flask_restplus import Api, fields, Resource
from model.analyzer import Analyzer
from services.areaservice import AreaService
from services.cacheservice import cache, Dictionaries
from services.cameraservice import CameraService
from services.eventservice import EventService
from services.analyzerservice import AnalyzerService

analyzer_service = AnalyzerService()
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

configuration_name_space = app.namespace('configuration')
device_name_space = app.namespace('device')
analyzer_name_space = app.namespace('analyzer')
events_name_space = app.namespace('event')
area_name_space = app.namespace('area')

camera_request = app.model('Camera configuration params', {
    'id': fields.String(required=True, description='Id of the camera'),
    'ip': fields.String(required=True, description='Camera ip address'),
    'user': fields.String(required=True, description='Camera user'),
    'password': fields.String(required=True, description='Password to camera')
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


@events_name_space.route("/timestamp")
class Events(Resource):
    @app.doc(params={'date_from': 'Oldest date from which events are downloaded'})
    def get(self):
        return str(time.time() * 1000)


@events_name_space.route("/events")
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


@device_name_space.route('')
class Device(Resource):
    @app.expect(camera_request)
    def post(self):
        """Create camera device"""
        id = request.json['id']
        ip = request.json['ip']
        username = request.json['user']
        password = request.json['password']
        camera_service.add_config(CameraConfig(id, ip, username, password))
        return {'success': True}, 200, {'ContentType': 'application/json'}


@device_name_space.route('/all')
class DeviceAll(Resource):
    def get(self):
        """Returns camera devices"""
        response = jsonify(camera_service.get_configs_json())
        response.headers.add('Access-Control-Allow-Origin', '*')
        return response


@device_name_space.route('/<string:id>')
class DeviceId(Resource):
    def get(self, id):
        """Returns camera device by given id"""
        return camera_service.get_config_json(id)

    def put(self, id):
        """Update camera device"""
        ip = request.json['ip']
        username = request.json['user']
        password = request.json['password']
        camera_service.update_config(id, ip, username, password)
        return {'success': True}, 200, {'ContentType': 'application/json'}

    def delete(self, id):
        """Delete camera device"""
        camera_service.delete_config(id)
        return {'success': True}, 200, {'ContentType': 'application/json'}


@device_name_space.route('/<string:id>/areas')
class DeviceIdAreas(Resource):
    def get(self, id):
        """Return list of areas for camera device of given id"""
        return area_service.get_areas_json(camera_id=id)

@device_name_space.route('/<string:id>/area')
class DeviceIdArea(Resource):

    @app.expect(area)
    def post(self, id):
        name = request.json['area_name']
        confidence_required = request.json['area_confidence_required']
        x = request.json['area_x']
        y = request.json['area_y']
        w = request.json['area_width']
        h = request.json['area_height']
        area_service.add_area(name, confidence_required, x, y, w, h, id)
        return {'success': True}, 200, {'ContentType': 'application/json'}


@device_name_space.route('/<string:id>/area/<name>')
class DeviceIdAreaName(Resource):
    def get(self, id, name):
        """Return area by name for camera device of given id"""
        return area_service.get_area_json(camera_id=id, area_name=name)

    @app.expect(area)
    def put(self, id, name):
        """Update area with given name for device of given id"""
        new_name = request.json['area_name']
        confidence_required = request.json['area_confidence_required']
        x = request.json['area_x']
        y = request.json['area_y']
        w = request.json['area_width']
        h = request.json['area_height']
        area_service.update_area(new_name, confidence_required, x, y, w, h, id, name)
        return {'success': True}, 200, {'ContentType': 'application/json'}

    def delete(self, id, name):
        """Delete area with given name for device of given id"""
        area_service.delete_area(id, name)
        return {'success': True}, 200, {'ContentType': 'application/json'}


@device_name_space.route('/<string:id>/image')
class DeviceIdImage(Resource):

    @staticmethod
    def send_image(image):
        file_object = io.BytesIO()
        image.save(file_object, 'PNG')
        file_object.seek(0)
        return send_file(file_object, mimetype='image/PNG')

    def get(self, id):
        """Returns image of camera device with given id"""
        image = analyzer_service.image(id)
        return self.send_image(image) if image else None


@analyzer_name_space.route('/state')
class States(Resource):
    def get(self):
        """Returns states of all cameras"""
        states = analyzer_service.state_all()
        return jsonify(states)


@analyzer_name_space.route("/state/<string:id>")
class StateId(Resource):
    def get(self, id):
        """Returns state of camera with given id"""
        return analyzer_service.state(id)


@analyzer_name_space.route("/on")
class StartAll(Resource):
    def post(self):
        """Start all cameras registered in the system"""
        success = analyzer_service.start_all()
        return {'success': success}, 200, {'ContentType': 'application/json'}


@analyzer_name_space.route('/on/<string:id>')
class StartId(Resource):
    @app.doc(params={'id': 'Camera id which will be started'})
    def post(self, id):
        """Start camera with given id"""
        success = analyzer_service.start(id)
        return {'success': success}, 200, {'ContentType': 'application/json'}


@analyzer_name_space.route('/off')
class StopCamera(Resource):
    def post(self):
        """Stop all analyzers"""
        success = analyzer_service.stop_all()
        return {'success': success}, 200, {'ContentType': 'application/json'}


@analyzer_name_space.route('/off/<string:id>')
class StopId(Resource):
    @app.doc(params={'id': 'Camera id which will be stopped'})
    def post(self, id):
        """Stop analyzer for camera with given id"""
        success = analyzer_service.stop(id)
        return {'success': success}, 200, {'ContentType': 'application/json'}


@area_name_space.route('')
class Area(Resource):
    def get(self):
        return area_service.get_areas_json()
