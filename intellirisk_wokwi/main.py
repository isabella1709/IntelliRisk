import machine
from machine import PWM, Pin, I2C
import dht
import time
from time import sleep_ms, ticks_ms 
import _thread
from i2c_lcd import I2cLcd 
from umqtt.simple import MQTTClient
import network

#declarando que o sensor está no pino 15 e é uma entrada
AddressOfLcd = 0x27
i2c = I2C(scl=Pin(26), sda=Pin(25), freq=400000)
lcd = I2cLcd(i2c, AddressOfLcd, 2, 16)
sensor = dht.DHT22(machine.Pin(15))
led_vermelho = Pin(27, Pin.OUT)
led_amarelo = Pin(12, Pin.OUT)
led_verde = Pin(14, Pin.OUT)

MQTT_CLIENT_ID = "teste"
MQTT_BROKER    = "broker.mqttdashboard.com"
MQTT_USER      = ""
MQTT_PASSWORD  = ""
MQTT_TOPIC1     = "dengue1"
MQTT_TOPIC2     = "dengue2"
MQTT_TOPIC3     = "dengue3"
MQTT_TOPIC4     = "topico_led"

print("Connecting to WiFi", end="")
sta_if = network.WLAN(network.STA_IF)
sta_if.active(True)
sta_if.connect('Wokwi-GUEST', '')
while not sta_if.isconnected():
  print(".", end="")
  time.sleep(0.1)
print(" Connected!")

print("Connecting to MQTT server... ", end="")
client = MQTTClient(MQTT_CLIENT_ID, MQTT_BROKER, user=MQTT_USER, password=MQTT_PASSWORD)
client.connect()

print("Connected!")

def mqtt_callback(topic, msg):
    if topic == b'topico_led' and msg == b'desligar':
        
        led_vermelho.off()
        led_amarelo.off()
        led_verde.off()
        lcd.clear()
        lcd.move_to(5,0)
        lcd.putstr('manutencao')
        time.sleep(5)

client.set_callback(mqtt_callback)
client.subscribe(b'topico_led')

def func():

    while True:

        client.check_msg()
        #Recebendo as mediçoes do sensor
        sensor.measure() 
        time.sleep(1)

        if sensor.humidity() > 70 and sensor.temperature() > 25:
            lcd.clear()
            lcd.move_to(5,0)
            lcd.putstr('Risco alto')
            lcd.move_to(5,1)
            lcd.putstr('de dengue!')
            led_verde.off()
            led_amarelo.off()
            led_vermelho.on()
            client.publish(MQTT_TOPIC1,"risco alto")
            client.publish(MQTT_TOPIC2, str(sensor.humidity()))
            client.publish(MQTT_TOPIC3, str(sensor.temperature()))

        elif sensor.humidity() > 70 or sensor.temperature() > 25:
            lcd.clear()
            lcd.move_to(5,0)
            lcd.putstr('Risco medio')
            lcd.move_to(5,1)
            lcd.putstr('de dengue!')
            led_amarelo.on()
            led_vermelho.off()
            led_verde.off()
            client.publish(MQTT_TOPIC1,"risco medio")
            client.publish(MQTT_TOPIC2, str(sensor.humidity()))
            client.publish(MQTT_TOPIC3, str(sensor.temperature()))

        else:
            lcd.clear()
            lcd.move_to(5,0)
            lcd.putstr('Risco baixo')
            lcd.move_to(5,1)
            lcd.putstr('de dengue!')
            led_verde.on()
            led_amarelo.off()
            led_vermelho.off()
            client.publish(MQTT_TOPIC1,"risco baixo")
            client.publish(MQTT_TOPIC2, str(sensor.humidity()))
            client.publish(MQTT_TOPIC3, str(sensor.temperature()))

_thread.start_new_thread(func,());