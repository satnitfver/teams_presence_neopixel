import network
import socket
import time
import secrets
from neopixel import Neopixel
from machine import Pin, reset, WDT
from umqtt.simple import MQTTClient

numpix = 12
strip = Neopixel(numpix, 0, 5, "GRB")

red = (255, 0, 0)
yellow = (255, 255, 0)
green = (0, 255, 0)
black = (0, 0, 0)
colors = {"busy": red, "away": yellow, "active": green, "offline": black} #match sts sent from PresenceLight API: ex:"BUSY" http://mqttbroker.local:1880/teams?status=busy

# MQTT settings
mqtt_broker = "10.x.x.x" #your broker IP
mqtt_port = 1883
mqtt_topic = b"teams/status/"
mqtt_client_id = "teams_status"
# mqtt_username = "your_username" #uncomment if you have user/pass
# mqtt_password = "your_password"

# Watchdog timer setup
wdt = WDT(timeout=8000)  # Set timeout to 8 seconds

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
            wdt.feed()  # Reset the watchdog timer
        except Exception as e:
            print("Error:", e)
            print("Reconnecting to MQTT broker...")
            connect_mqtt()  # Attempt to reconnect if failed to connect
        time.sleep(1)

while True:
    try:
        connect_wifi()
        connect_mqtt()
        mqtt_loop()  # Start MQTT loop
    except Exception as e:
        print("Error:", e)
        print("Resetting the system...")
        reset()  # Reset the system on error, this will loop if network drops, test without
