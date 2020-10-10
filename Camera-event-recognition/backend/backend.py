from flask import Flask, request, render_template
from model.receiver import CameraAnalyzer, DetectBox
from model.repository import Repository
from config.configurator import Configurator
from config.configuration import Configuration

DATABASE = "events"

repository = Repository(DATABASE)

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
        batch_size = request.form['batch_size']
        configuration = Configuration(camera_ip, camera_user, camera_password, batch_size)
        Configurator().add_configuration(configuration)


@app.route('/configs')
def configs():
    return Configurator().get_configurations()


@app.route('/start')
def start():
    return ""


@app.route('/stop')
def stop():
    return ""
