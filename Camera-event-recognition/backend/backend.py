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


@app.route("/database")
def database():
    return repository.read()


@app.route('/config/add', methods=['POST'])
def config():
    if request.method == 'POST':
        camera_ip = request.form['camera_ip'],
        camera_user = request.form['camera_user']
        camera_password = request.form['camera_password']
        configuration = Configuration.from_arguments(camera_ip, camera_user, camera_password)
        Configurator().add_configuration(configuration)


@app.route('/config/get/<camera_id>')
def get_config(camera_id):
    configuration = Configurator().find_configuration(camera_id)
    return str(configuration)


@app.route('/configs')
def configs():
    cs = Configurator().get_configurations()
    cl = [str(c) for c in cs.values()]
    return str(cl)


@app.route('/start/<camera_id>')
def start(camera_id):
    configuration = Configurator().find_configuration(camera_id)
    if configuration is None:
        return "Receiver not found"
    else:
        camera_analyzer = CameraAnalyzer(configuration)
        thread = threading.Thread(target=camera_analyzer.video, args=(True, True, ))
        thread.start()
        receivers[camera_id] = thread
        return "Analyzer " + camera_id + " started!"


@app.route('/stop/<camera_id>')
def stop(camera_id):
    thread: threading = receivers[camera_id]
    thread.stop()
    return "Analyzer " + camera_id + " stopped"
