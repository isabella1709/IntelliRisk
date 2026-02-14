from flask import Blueprint, request, render_template
from models.iot.sensors import Sensor
from models.iot.read import Read
import flask_login
from flask_login import current_user

sensors = Blueprint("sensors",__name__, template_folder="views")

@sensors.route('/register_sensores')
@flask_login.login_required
def register_sensores():
    return render_template("register_sensores.html", roles=current_user.role_id)

@sensors.route('/add_sensor', methods=['POST'])
@flask_login.login_required
def add_sensors():
    sensor = request.form['sensor']
    localizacao = request.form['localizacao']
    brand = request.form['brand']
    model = request.form['model']
    topic = request.form['topic']
    unit = request.form['unit']

    is_active = True if request.form.get("is_active") == "on" else False

    Sensor.save_sensor(sensor, brand, model, is_active, unit, topic, localizacao)
    
    sensors = Sensor.get_sensors()
    return render_template("sensores.html", devices = sensors, roles=current_user.role_id)

@sensors.route('/sensores')
@flask_login.login_required
def sensors_():
    sensors = Sensor.get_sensors()
    return render_template("sensores.html", devices=sensors, roles=current_user.role_id)

@sensors.route('/edit_sensor')
@flask_login.login_required
def edit_sensor():
    id = request.args.get('id', None)
    sensor = Sensor.get_single_sensor(id)
    return render_template("update_sensor.html", sensor = sensor, roles=current_user.role_id)

@sensors.route('/update_sensor', methods=['POST'])
@flask_login.login_required
def update_sensor():
    id = request.form.get("id")
    name = request.form.get("sensor")
    brand = request.form.get("brand")
    model = request.form.get("model")
    topic = request.form.get("topic")
    unit = request.form.get("unit")
    localizacao = request.form.get("localizacao")
    is_active = True if request.form.get("is_active") == "on" else False
    sensors = Sensor.update_sensor(id, name, brand, model, topic, unit, is_active, localizacao)
    return render_template("sensores.html", devices = sensors, roles=current_user.role_id)

@sensors.route('/del_sensor', methods=['GET'])
@flask_login.login_required
def del_sensor():
    id = request.args.get('id', None)
    Read.delete_read(id)
    sensors = Sensor.delete_sensor(id)
    return render_template("sensores.html", devices = sensors, roles=current_user.role_id)

@sensors.route('/list_sensors')
@flask_login.login_required
def list_sensors():
    sensors = Sensor.get_sensors()
    return render_template("list_sensors.html", devices=sensors, roles=current_user.role_id)