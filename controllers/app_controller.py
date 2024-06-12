#app_controller.py
# from flask import Flask, render_template, request
from flask import *

from controllers.login_controller import login_
from controllers.sensors_controller import sensors
from controllers.actuators_controller import actuators
from controllers.reads_controller import read
from controllers.writes_controller import write
from models.user.users import User
from models.iot.read import Read
from models.iot.write import Write
from controllers.users_controller import user

import flask_login
from flask_login import LoginManager, logout_user, current_user, login_required

from models.db import db, instance

from flask_mqtt import Mqtt
from flask_socketio import SocketIO
import json

import flask_login
from flask_login import current_user

temperatura= 22
humidade= 40
risco = "risco baixo"

def create_app():
    app = Flask(__name__,
    template_folder="./views/",
    static_folder="./static/",
    root_path="./")

    app.config['TESTING'] = False
    app.config['SECRET_KEY'] = 'generated-secrete-key'
    app.config['SQLALCHEMY_DATABASE_URI'] = instance
    db.init_app(app)

    # blueprint
    app.register_blueprint(login_, url_prefix='/')
    app.register_blueprint(sensors, url_prefix='/')
    app.register_blueprint(actuators, url_prefix='/')
    app.register_blueprint(user, url_prefix='/')
    app.register_blueprint(read, url_prefix='/')
    app.register_blueprint(write, url_prefix='/')



    app.config['MQTT_BROKER_URL'] = 'broker.mqttdashboard.com'
    #app.config['MQTT_BROKER_URL'] = 'mqtt-dashboard.com'
    #app.config['MQTT_BROKER_URL'] = '192.168.0.77'
    app.config['MQTT_BROKER_PORT'] = 1883
    app.config['MQTT_USERNAME'] = ''
    app.config['MQTT_PASSWORD'] = '' 
    app.config['MQTT_KEEPALIVE'] = 5000 
    app.config['MQTT_TLS_ENABLED'] = False

    mqtt_client= Mqtt()
    mqtt_client.init_app(app)
    topic_subscribe = "/dengue1"


    app.secret_key = 'd54gdh543trg@!54gdh'
    login_manager = flask_login.LoginManager()
    login_manager.init_app(app)

    dengue_values = {
    "dengue1": None,
    "dengue2": None,
    "dengue3": None,
    "topico_led": None
    }
    
    @app.route('/publish')
    def publish():
        return render_template("publish.html", roles=current_user.role_id)
    

    @app.route('/tempo_real')
    def tempo_real():
        global risco, humidade, temperatura
        values = {
        "dengue1": dengue_values["dengue1"],
        "dengue2": dengue_values["dengue2"],
        "dengue3": dengue_values["dengue3"],
        }

        print("Values:", values)
        return render_template("interacao.html", values=values, roles=current_user.role_id)

    
    @mqtt_client.on_connect()
    def handle_connect(client, userdata, flags, rc):
        if rc == 0:
            print('Broker Connected successfully')
            mqtt_client.subscribe("dengue1")
            mqtt_client.subscribe("dengue2")
            mqtt_client.subscribe("dengue3")
            mqtt_client.subscribe("topico_led")
        else:
            print('Bad connection. Code:', rc)

    @mqtt_client.on_message()
    def handle_mqtt_message(client, userdata, message):
        if message.topic in ["dengue1", "dengue2", "dengue3", "topico_led"]:
            payload = message.payload.decode()
            print(payload)
            try:
                with app.app_context():
                    try:
                        Read.save_read(message.topic, payload)
                        print(f"Read saved for {message.topic} with payload: {payload}")
                    except Exception as e:
                        print(f"Failed to save Read for {message.topic}: {e}")

                    try:
                        Write.save_write(message.topic, payload)
                        print(f"Write saved for {message.topic} with payload: {payload}")
                    except Exception as e:
                        print(f"Failed to save Write for {message.topic}: {e}")

                    if message.topic == "dengue1":
                        dengue_values['dengue1'] = str(payload)
                    elif message.topic == "dengue2":
                        dengue_values['dengue2'] = float(payload)
                    elif message.topic == "dengue3":
                        dengue_values['dengue3'] = float(payload)
                    elif message.topic == "topico_led":
                        dengue_values['topico_led'] = str(payload)
                    print(f"Updated {message.topic} to {dengue_values[message.topic]}")
            except Exception as e:
                print(f"Error handling message for {message.topic}: {e}")

    @login_manager.user_loader
    def get_user(user_id):
        return User.query.filter_by(id=user_id).first()


    '''@mqtt_client.on_message()
    def handle_mqtt_message(client, userdata, message):
        global risco, humidade, temperatura
        if message.topic == "dengue1":
            risco = message.payload.decode()
        elif message.topic == "dengue2":
            humidade = float(message.payload.decode())
        elif message.topic == "dengue3":
            temperatura = float(message.payload.decode())'''

    @app.route('/desligar_led', methods=['POST'])
    def desligar_led():
        global risco, humidade, temperatura
        values = {"risco": risco, "humidade": humidade, "temperatura": temperatura}
        mqtt_client.publish("topico_led", "desligar")
        return render_template("publish.html", values=values, roles=current_user.role_id)
    
    @app.route('/publish_message', methods = ['GET','POST'])
    def publish_message():

        request_data = request.get_json()

        topic = request_data['topic']
        message = request_data['message']

        publish_result = mqtt_client.publish(topic,message)
        try:
            with app.app_context():
                Write.save_write(topic, message)
        except:
            pass

        return jsonify(publish_result)

    @app.route('/')
    def index():
        return render_template('index.html')

    @app.route('/login')
    def login():
        return render_template('login.html')

    @app.route('/adm')
    def adm():
        return render_template('adm.html', roles=current_user.role_id)

    @app.errorhandler(401)
    def page_not_found(error):
        return render_template('erro.html'), 401

    @app.errorhandler(403)
    def page_not_found(error):
        return render_template('erro.html'), 403

    @app.errorhandler(404)
    def page_not_found(error):
        return render_template('erro.html'), 404

    @app.errorhandler(408)
    def page_not_found(error):
        return render_template('erro.html'), 408

    @app.errorhandler(429)
    def page_not_found(error):
        return render_template('erro.html'), 429

    @app.errorhandler(500)
    def page_not_found(error):
        return render_template('erro.html'), 500

    @app.errorhandler(503)
    def page_not_found(error):
        return render_template('erro.html'), 503
    
    return app