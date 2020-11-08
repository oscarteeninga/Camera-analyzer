import multiprocessing
from services.cameraservice import CameraService
from config.cameraconfig import CameraConfig
from services.eventservice import EventService
from services.areaservice import AreaService
from flask import Flask, request, render_template, jsonify
from model.receiver import CameraAnalyzer

receivers = {}

app = Flask(__name__)

event_service = EventService()
area_service = AreaService()
camera_service = CameraService()


@app.route("/")
def index():
    return render_template('index.html')


@app.route('/config/add', methods=['POST'])
def add_config():
    ip = request.form['camera_ip']
    username = request.form['camera_user']
    password = request.form['camera_password']
    fps = request.form['camera_fps']
    camera_service.add_config(CameraConfig(ip, username, password, fps))


@app.route('/config/<camera_id>')
def get_config(camera_id):
    return jsonify(camera_service.get_config(camera_id))


@app.route('/configs')
def get_configs():
    return jsonify(list(camera_service.get_configs()))


@app.route('/devices')
def devices():
    return jsonify(list(camera_service.get_ips()))


@app.route('/state')
def state():
    states = {}
    for conf in camera_service.get_configs():
        s = "off"
        if receivers.get(conf):
            s = "on"
        states[conf] = s
    return jsonify(states)


@app.route('/state/<camera_id>')
def state_single_camera(camera_id):
    conf = camera_service.get_config(camera_id)
    if conf is None:
        return "Camera does not exists", 404
    elif conf in receivers.keys():
        return jsonify("on")
    else:
        return jsonify("off")


@app.route('/events', methods=['GET'])
def events():
    date_from = request.args.get("date_from")
    return event_service.get_events(date_from)


@app.route('/on', methods=['POST'])
def start():
    for conf in camera_service.get_configs():
        camera_analyzer = CameraAnalyzer(conf)
        process = multiprocessing.Process(target=camera_analyzer.video, args=(True, True,))
        process.start()
        receivers[conf] = process
        return ""


@app.route('/on/<camera_id>', methods=['POST'])
def start_single_camera(camera_id):
    conf = camera_service.get_config(camera_id)
    if conf is None:
        return "Receiver not found", 404
    elif conf in receivers.keys():
        return "Analyzer already started"
    else:
        camera_analyzer = CameraAnalyzer(conf)
        process = multiprocessing.Process(target=camera_analyzer.video, args=(True, True,))
        process.start()
        receivers[conf] = process
        return "Analyzer " + camera_id + " started!"


@app.route('/off', methods=['POST'])
def stop():
    for process in receivers:
        process.terminate()
    receivers.clear()
    return ""


@app.route('/off/<camera_id>', methods=['POST'])
def stop_single_camera(camera_id):
    conf = camera_service.get_config(camera_id)
    if conf is None:
        return "Receiver not found"
    elif conf not in receivers.keys():
        return "Analyzer already stopped"
    else:
        receivers[conf].terminate()
        receivers.pop(conf)
        return "Analyzer " + camera_id + " stopped"


@app.route('/areas', methods=['GET'])
def areas():
    return jsonify(area_service.get_areas())
