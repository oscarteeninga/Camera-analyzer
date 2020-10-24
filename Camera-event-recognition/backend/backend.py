from flask import Flask, request, render_template
from model.repository import Repository
from model.receiver import CameraAnalyzer
from config.configurator import Configurator
from config.configuration import Configuration
import threading

DATABASE = "events"

repository = Repository(DATABASE)
receivers = {}

app = Flask(__name__)


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
    return str(list(Configurator().get_configurations().keys()))


@app.route('/state')
def state():
    config_ips = Configurator().get_configurations().keys()
    states = {}
    for config_ip in config_ips:
        s = "off"
        if receivers.get(config_ip):
            s = "on"
        states[config_ip] = s
    return str(states)


@app.route('/on/<camera_id>')
def start(camera_id):
    configuration = Configurator().find_configuration(camera_id)
    if configuration is None:
        return "Receiver not found"
    else:
        camera_analyzer = CameraAnalyzer(configuration)
        thread = threading.Thread(target=camera_analyzer.video, args=(True, True,))
        thread.start()
        receivers[camera_id] = thread
        return "Analyzer " + camera_id + " started!"


@app.route('/off/<camera_id>')
def stop(camera_id):
    thread: threading = receivers.get(camera_id)
    # thread.stop() ##TODO
    receivers[camera_id] = None
    return "Analyzer " + camera_id + " stopped"
