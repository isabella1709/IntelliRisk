from models.db import db
from models.iot.devices import Device

class Sensor(db.Model):
    __tablename__ = 'sensors'
    id = db.Column('id', db.Integer, primary_key=True)
    devices_id = db.Column( db.Integer, db.ForeignKey(Device.id))
    unit = db.Column(db.String(50))
    topic = db.Column(db.String(50))
    localizacao = db.Column(db.String(100))

    def save_sensor(name, brand, model, is_active, unit, topic, localizacao):
        device = Device(name = name, brand = brand, model = model, is_active = is_active)
        sensor = Sensor(devices_id = device.id, unit = unit, topic = topic, localizacao = localizacao)
        device.sensors.append(sensor)
        db.session.add(device)
        db.session.commit()

    def get_sensors():
        sensors = Sensor.query.join(Device, Device.id == Sensor.devices_id)\
        .add_columns(Device.id, Device.name, Device.brand, Device.model, Device.is_active, 
                     Sensor.topic, Sensor.unit, Sensor.localizacao).all()
        return sensors
    
    def get_single_sensor(id):
        sensor = Sensor.query.filter(Sensor.devices_id == id).first()
        if sensor is not None:
            sensor = Sensor.query.filter(Sensor.devices_id == id)\
        .join(Device).add_columns(Device.id, Device.name, Device.brand,
        Device.model, Device.is_active, Sensor.topic, Sensor.unit, Sensor.localizacao).first()
            return [sensor]
        
    def update_sensor(id,name, brand, model, topic, unit, is_active, localizacao):
        device = Device.query.filter(Device.id == id).first()
        sensor = Sensor.query.filter(Sensor.devices_id == id).first()
        if device is not None:
            device.name = name
            device.brand = brand
            device.model = model
            sensor.topic = topic
            sensor.unit = unit
            device.is_active = is_active
            sensor.localizacao = localizacao
            db.session.commit()
            return Sensor.get_sensors()
    
    def delete_sensor(id):
        device = Device.query.filter(Device.id == id).first()
        sensor = Sensor.query.filter(Sensor.devices_id == id).first()
        db.session.delete(sensor)
        db.session.delete(device)
        db.session.commit()
        return Sensor.get_sensors()