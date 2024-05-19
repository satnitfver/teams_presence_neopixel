import network
import socket
import time
import secrets
from neopixel import Neopixel
from machine import Pin
from umqtt.simple import MQTTClient

numpix = 12
strip = Neopixel(numpix, 0, 5, "GRB")

red = (255, 0, 0)
yellow = (255, 255, 0)
green = (0, 255, 0)
black = (0, 0, 0)
colors = {"busy": red, "away": yellow, "active": green, "offline": black}

# MQTT settings
mqtt_broker = "10.0.0.0"
mqtt_port = 1883
mqtt_topic = b"teams/status/"
mqtt_client_id = "teams_status"
#mqtt_username = "your_username"
#mqtt_password = "your_password"

def on_message(topic, message):
    status = message.decode()
    print("Received message:", str(status))
    color = colors.get(status, black)
    set_color(color)

def set_color(color):
    for i in range(numpix):
        strip.set_pixel(i, color)
    strip.show()

def connect_wifi():
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect(secrets.SSID, secrets.PASSWORD)
    max_wait = 15
    while max_wait > 0:
        if wlan.isconnected():
            break
        max_wait -= 1
        time.sleep(1)
    if not wlan.isconnected():
        raise RuntimeError('WiFi connection failed')
    print('Connected to WiFi')

def connect_mqtt():
    global client
    client = MQTTClient(mqtt_client_id, mqtt_broker, mqtt_port, keepalive=3600)
    client.set_callback(on_message)
    client.connect()
    client.subscribe(mqtt_topic)
    print("Connected to MQTT broker")

def mqtt_loop():
    while True:
        try:
            client.check_msg()  # Check for MQTT messages
        except Exception as e:
            print("Error:", e)
            print("Reconnecting to MQTT broker...")
            connect_mqtt()  # Attempt to reconnect
        time.sleep(1)

connect_wifi()   
connect_mqtt()

try:        
    mqtt_loop()  # Start MQTT loop
except Exception as e:
    print("Error:", e)


