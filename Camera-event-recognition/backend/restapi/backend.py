import io
import time

from flask import Flask, request, jsonify, send_file, Response
from flask_cors import CORS
from flask_restplus import Api, fields, Resource
from services.analyzerservice import AnalyzerService
from services.areaservice import AreaService
from services.cameraservice import CameraService
from services.eventservice import EventService

event_service = EventService()
area_service = AreaService(event_service)
camera_service = CameraService(area_service)
analyzer_service = AnalyzerService(event_service, camera_service, area_service)

flask_app = Flask(__name__)
CORS(flask_app)
app = Api(app=flask_app, title="Camera Api", default="Camera Api", default_label="Camera Api")

configuration_name_space = app.namespace('configuration')
device_name_space = app.namespace('devices')
events_name_space = app.namespace('events')
area_name_space = app.namespace('areas')

camera_request = app.model('Camera configuration params', {
    'name': fields.String(required=True, description='Id of the camera'),
    'ip': fields.String(required=True, description='Camera ip address'),
    'user': fields.String(required=True, description='Camera user'),
    'password': fields.String(required=True, description='Password to camera')
})

area = app.model('Area configuration params', {
    'coverage_required': fields.Float(required=True, description='coverage needed to register event'),
    'x': fields.Integer(required=True, description='X cord of start of area'),
    'y': fields.Integer(required=True, description='Y cord of start of area'),
    'width': fields.Integer(required=True, description='The width of area'),
    'height': fields.Integer(required=True, description='The height of area')
})


@app.route("/timestamp")
class Events(Resource):
    """Returns timestamp of application"""

    def get(self):
        return str(time.time() * 1000)


@events_name_space.route("")
class Events(Resource):
    @app.doc(params={'date_from': 'Oldest date from which events are downloaded'})
    @app.doc(params={'page': 'Events are taken from given offset'})
    @app.doc(params={'size': 'Maximum number of events in response'})
    def get(self):
        """Return list of events"""
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
        name = request.json['name']
        ip = request.json['ip']
        username = request.json['user']
        password = request.json['password']
        camera_service.add_config(name, ip, username, password)
        return {'success': True}, 200, {'ContentType': 'application/json'}

    def get(self):
        """Returns camera devices"""
        response = jsonify(camera_service.get_configs_json())
        return response


@device_name_space.route('/<string:id>')
class DeviceId(Resource):
    @app.doc(params={'id': 'Id of device'})
    def get(self, id):
        """Returns camera device by given id"""
        return camera_service.get_config_json(id)

    @app.expect(camera_request)
    def put(self, id):
        """Update camera device"""
        name = request.json['name']
        ip = request.json['ip']
        username = request.json['user']
        password = request.json['password']
        camera_service.update_config(id, name, ip, username, password)
        return {'success': True}, 200, {'ContentType': 'application/json'}

    @app.doc(params={'id': 'Id of device'})
    def delete(self, id):
        """Delete camera device"""
        camera_service.delete_config(id)
        return {'success': True}, 200, {'ContentType': 'application/json'}


@device_name_space.route('/<string:id>/areas')
class DeviceIdAreas(Resource):
    @app.doc(params={'id': 'Id of device'})
    def get(self, id):
        """Return list of areas for camera device of given id"""
        return area_service.get_areas_json(camera_id=id)

    @app.expect(area)
    def post(self, id):
        """Add area to device"""
        coverage_required = request.json['coverage_required']
        x = request.json['x']
        y = request.json['y']
        w = request.json['width']
        h = request.json['height']
        coverage_required = float(coverage_required) / 100
        area_service.insert_area(coverage_required, x, y, w, h, id)
        return {'success': True}, 200, {'ContentType': 'application/json'}


@device_name_space.route('/<string:id>/img')
class DeviceIdImage(Resource):

    @staticmethod
    def send_image(image):
        file_object = io.BytesIO()
        image.save(file_object, 'PNG')
        file_object.seek(0)
        return send_file(file_object, mimetype='image/PNG')

    @app.doc(params={'id': 'Id of device'})
    def get(self, id):
        """Returns image of camera device with given id"""
        return Response(camera_service.get_image(id),
                        mimetype="multipart/x-mixed-replace; boundary=frame")


@device_name_space.route('/<string:id>/video')
class DeviceIdImage(Resource):

    @staticmethod
    def send_image(image):
        file_object = io.BytesIO()
        image.save(file_object, 'PNG')
        file_object.seek(0)
        return send_file(file_object, mimetype='image/PNG')

    @app.doc(params={'id': 'Id of device'})
    def get(self, id):
        """Returns image of camera device with given id"""
        return Response(camera_service.get_video(id),
                        mimetype="multipart/x-mixed-replace; boundary=frame")


@app.route('/state')
class States(Resource):
    def get(self):
        """Returns states of all cameras"""
        states = analyzer_service.state_all()
        return jsonify(states)


@app.route("/state/<string:id>")
class StateId(Resource):
    @app.doc(params={'id': 'Id of device'})
    def get(self, id):
        """Returns state of camera with given id"""
        return analyzer_service.state(id)


@app.route("/on")
class StartAll(Resource):
    def post(self):
        """Start all cameras registered in the system"""
        success = analyzer_service.start_all()
        return {'success': success}, 200, {'ContentType': 'application/json'}


@app.route('/on/<string:id>')
class StartId(Resource):
    @app.doc(params={'id': 'Camera id which will be started'})
    def post(self, id):
        """Start camera with given id"""
        success = analyzer_service.start(id)
        return {'success': success}, 200, {'ContentType': 'application/json'}


@app.route('/off')
class StopCamera(Resource):
    def post(self):
        """Stop all analyzers"""
        success = analyzer_service.stop_all()
        return {'success': success}, 200, {'ContentType': 'application/json'}


@app.route('/off/<string:id>')
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


@area_name_space.route('/<string:id>')
class AreaId(Resource):
    @app.doc(params={'id': 'Id of area'})
    def get(self, id):
        """Returns single area by id"""
        return area_service.get_area_json(id)

    @app.expect(area)
    def put(self, id):
        """Update area with given name for device of given id"""
        coverage_required = request.json['coverage_required']
        x = request.json['x']
        y = request.json['y']
        w = request.json['width']
        h = request.json['height']
        coverage_required = float(coverage_required) / 100
        area_service.update_area(id, coverage_required, x, y, w, h)
        return {'success': True}, 200, {'ContentType': 'application/json'}

    def delete(self, id):
        """Delete area with given id"""
        area_service.delete_area(id)
