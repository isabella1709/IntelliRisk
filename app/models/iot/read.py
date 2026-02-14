from models.db import db
from models.iot.sensors import Sensor
from models.iot.devices import Device
from datetime import datetime

class Read(db.Model):
    __tablename__ = 'read'
    id= db.Column('id', db.Integer, nullable = False, primary_key=True)
    read_datetime = db.Column(db.DateTime(), nullable = False)
    sensors_id= db.Column(db.Integer, db.ForeignKey(Sensor.id), nullable = False)
    value = db.Column( db.Float, nullable = True)

    def save_read(topic, value):
        sensor = Sensor.query.filter(Sensor.topic == topic).first()
        device = Device.query.filter(Device.id == sensor.devices_id).first()
        if (sensor is not None) and (device.is_active==True):
            #read = Read( read_datetime = datetime.now(), sensors_id = sensor.id, value = float(value) )
            read = Read( read_datetime = datetime.now(), sensors_id = sensor.id, value = value)
            db.session.add(read)
            db.session.commit()

    def get_read(device_id, start, end):
        sensor = Sensor.query.filter(Sensor.devices_id == device_id).first()
        read = Read.query.filter(Read.sensors_id == sensor.id, Read.read_datetime > start, Read.read_datetime<end).all()
        return read
    
    def delete_read(id):
        try:
            sensor = Sensor.query.filter(Sensor.devices_id == id).first()
            read = Read.query.filter(Read.sensors_id == sensor.id).first()
            db.session.delete(read)
            db.session.commit()
        except Exception as e:
            print(f"DELETE WRITE ==== {e}")