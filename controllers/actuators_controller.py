from flask import Blueprint, request, render_template
from models.iot.actuators import Actuator
from models.iot.write import Write

import flask_login
from flask_login import current_user

actuators = Blueprint("actuators",__name__, template_folder="templates")

@actuators.route('/register_atuadores')
@flask_login.login_required
def register_atuadores():
    return render_template("register_atuadores.html", roles=current_user.role_id)

@actuators.route('/add_actuator', methods=['POST'])
@flask_login.login_required
def add_actuators():
    actuator = request.form['atuador']
    localizacao = request.form['localizacao']
    brand = request.form['brand']
    model = request.form['model']
    topic = request.form['topic']
    unit = request.form['unit']

    is_active = True if request.form.get("is_active") == "on" else False

    Actuator.save_actuator(actuator, brand, model, is_active, unit, topic, localizacao)
    
    atuadores = Actuator.get_actuators()
    return render_template("atuadores.html", devices = atuadores, roles=current_user.role_id)

@actuators.route('/atuadores')
@flask_login.login_required
def atuadores_():
    atuadores = Actuator.get_actuators()
    return render_template("atuadores.html", devices=atuadores, roles=current_user.role_id)

@actuators.route('/edit_actuator')
@flask_login.login_required
def edit_actuator():
    id = request.args.get('id', None)
    actuator = Actuator.get_single_actuator(id)
    return render_template("update_actuator.html", actuator = actuator, roles=current_user.role_id)

@actuators.route('/update_actuator', methods=['POST'])
@flask_login.login_required
def update_actuator():
    id = request.form.get("id")
    name = request.form.get("actuator")
    brand = request.form.get("brand")
    model = request.form.get("model")
    topic = request.form.get("topic")
    unit = request.form.get("unit")
    localizacao = request.form.get("localizacao")
    is_active = True if request.form.get("is_active") == "on" else False
    actuators = Actuator.update_actuator(id, name, brand, model, topic, unit, is_active, localizacao)
    return render_template("atuadores.html", devices = actuators, roles=current_user.role_id)

@actuators.route('/del_actuator', methods=['GET'])
@flask_login.login_required
def del_actuator():
    id = request.args.get('id', None)
    Write.delete_write(id)
    actuators = Actuator.delete_actuator(id)
    return render_template("atuadores.html", devices = actuators, roles=current_user.role_id)

@actuators.route('/list_actuators')
@flask_login.login_required
def list_actuators():
    atuadores = Actuator.get_actuators()
    return render_template("list_actuators.html", devices=atuadores, roles=current_user.role_id)