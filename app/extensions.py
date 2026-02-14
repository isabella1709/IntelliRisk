from flask_login import LoginManager
from flask_mqtt import Mqtt
from models.db import db

login_manager = LoginManager()
mqtt = Mqtt()
