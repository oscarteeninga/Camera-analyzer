from flask import Flask, request, render_template
from model.repository import Repository
from config.configurator import Configurator
from config.configuration import Configuration

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


@app.route('/configs')
def configs():
    return Configurator().get_configurations()


@app.route('/start/<camera_id>')
def start(camera_id):
    configuration = Configurator().find_configuration(camera_id)
    if configuration is None:
        return "Receiver not found"
    else:
        return "Analyzer started!"


@app.route('/stop/<camera_id>')
def stop(camera_id):
    return ""
