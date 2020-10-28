import threading

from config.configuration import Configuration
from config.configurator import Configurator
from eventservice import EventService
from flask import Flask, request, render_template, jsonify
from model.receiver import CameraAnalyzer

receivers = {}

app = Flask(__name__)

eventservice = EventService()


@app.route("/")
def index():
    return render_template('index.html')


@app.route('/config/add', methods=['POST'])
def add_config():
    if request.method == 'POST':
        camera_ip = request.form['camera_ip'],
        camera_user = request.form['camera_user']
        camera_password = request.form['camera_password']
        configuration = Configuration.from_arguments(camera_ip, camera_user, camera_password)
        Configurator().add_configuration(configuration)


@app.route('/config/<camera_id>')
def config(camera_id):
    return str(Configurator().find_configuration(camera_id))


@app.route('/configs')
def configs():
    cs = Configurator().get_configurations()
    cl = [str(c) for c in cs.values()]
    return str(cl)


@app.route('/devices')
def devices():
    return jsonify(list(Configurator().get_configurations().keys()))


@app.route('/state')
def state():
    config_ips = Configurator().get_configurations().keys()
    states = {}
    for config_ip in config_ips:
        s = "off"
        if receivers.get(config_ip):
            s = "on"
        states[config_ip] = s
    return jsonify(states)


@app.route('/state/<camera_id>')
def state_single_camera(camera_id):
    config_ips = Configurator().get_configurations().keys()
    if camera_id not in config_ips:
        return "", 404
    if receivers.get(camera_id):
        return jsonify("on")
    else:
        return jsonify("off")


@app.route('/events')
def events():
    return jsonify(eventservice.get_events())


@app.route('/on', methods=['POST'])
def start():
    for conf in Configurator.get_configurations():
        camera_analyzer = CameraAnalyzer(conf.camera_id)
        thread = threading.Thread(target=camera_analyzer.video, args=(True, True,))
        thread.start()
        receivers[conf.camera_id] = thread
        return ""


@app.route('/on/<camera_id>', methods=['POST'])
def start_single_camera(camera_id):
    configuration = Configurator().find_configuration(camera_id)
    if configuration is None:
        return "Receiver not found", 404
    else:
        # TODO check if already started
        camera_analyzer = CameraAnalyzer(configuration)
        thread = threading.Thread(target=camera_analyzer.video, args=(True, True,))
        thread.start()
        receivers[camera_id] = thread
        return "Analyzer " + camera_id + " started!"


@app.route('/off', methods=['POST'])
def stop():
    for thread in receivers:
        pass
        # todo thread.stop()
    receivers.clear()
    return ""


@app.route('/off/<camera_id>', methods=['POST'])
def stop_single_camera(camera_id):
    thread: threading = receivers.get(camera_id)
    # thread.stop() ##TODO
    receivers[camera_id] = None
    return "Analyzer " + camera_id + " stopped"
