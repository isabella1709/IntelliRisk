from models.db import db
from models.iot.actuators import Actuator
from models.iot.devices import Device
from datetime import datetime

class Write(db.Model):
    __tablename__ = 'write'
    id = db.Column('id', db.Integer, nullable = False, primary_key=True)
    write_datetime = db.Column(db.DateTime(), nullable = False)
    actuators_id= db.Column(db.Integer, db.ForeignKey(Actuator.id), nullable = False)
    value = db.Column( db.String(255), nullable = True)

    def save_write(topic, value):
        actuator = Actuator.query.filter(Actuator.topic == topic).first()
        print(actuator)
        device = Device.query.filter(Device.id == actuator.devices_id).first()
        print(device)
        if (actuator is not None) and (device.is_active==True):
            write = Write(write_datetime = datetime.now(), actuators_id = actuator.id, value = value )
            print("oi")
            db.session.add(write)
            db.session.commit()

    def get_write(device_id, start, end):
        actuator = Actuator.query.filter(Actuator.devices_id == device_id).first()
        print(actuator)
        write = Write.query.filter(Write.actuators_id == actuator.id,
        Write.write_datetime > start,
        Write.write_datetime<end).all()
        print(write)
        return write
    
    def delete_write(id):
        try:
            actuator = Actuator.query.filter(Actuator.devices_id == id).first()
            write = Write.query.filter(Write.actuators_id == actuator.id).first()
            db.session.delete(write)
            db.session.commit()
        except Exception as e:
            print(f"DELETE WRITE ==== {e}")