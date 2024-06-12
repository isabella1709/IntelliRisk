from flask import Flask
from models import *

def create_db(app:Flask):
    with app.app_context():
        db.drop_all()
        db.create_all()

        Sensor.save_sensor("Sensor de umidade", "TJ's", "1.0", 1, "Oi", "dengue2", "Santa Felicidade")
        Sensor.save_sensor("Sensor de temperatura", "TJ's", "1.5", 1, "Oi", "dengue3", "Santa Felicidade")
        
        Actuator.save_actuator("Led", "TJ's", "3.5", 1, "Oi", "topico_led", "Santa Felicidade")
        Actuator.save_actuator("Display LCD", "TJ's", "2.0", 1, "Oi", "dengue1", "Santa Felicidade")

        Role.save_role( "Admin", "Usuário full" )
        Role.save_role( "Estatístico", "Visualizar dados em tempo real vindo do MQTT broker; Acesso a tela com dados históricos dos sensores;")
        Role.save_role( "Operador", "Acesso a tela de comandos remotos; Acesso a tela de dados históricos de atuações remotas;")

        User.save_user("Admin", "dengue", "dengue", "dengue01")
        User.save_user("Estatístico", "ana", "ana", "dengue")
        User.save_user("Estatístico", "isa", "isa", "dengue")
        User.save_user("Operador", "mi", "mi", "dengue")
        User.save_user("Operador", "ye", "ye", "dengue")

        Read.save_read("dengue2", 20.0)
        Write.save_write("topico_led", 40.0)
        Write.save_write("dengue1", 40.0)

