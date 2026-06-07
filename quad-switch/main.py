from machine import Pin
import network
import time
from umqtt.simple import MQTTClient
import secrets

MQTT_TOPIC  = "homeassistant/device/quad-switch/{}"
BUTTON_PINS = [0, 1, 2, 3]
LED_PINS    = [4, 20]
STATUS_LED  = Pin(15, Pin.OUT)

Pin(5, Pin.OUT).value(0)  # GPIO5 as GND reference (orange wire)

buttons = [Pin(p, Pin.IN, Pin.PULL_UP) for p in BUTTON_PINS]
leds    = [Pin(p, Pin.OUT) for p in LED_PINS]

def toggle_status(state):
    STATUS_LED.value(1 if state else 0)

def connect_wifi():
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect(secrets.WIFI_SSID, secrets.WIFI_PASSWORD)
    print("Connecting to WiFi", end="")
    while not wlan.isconnected():
        print(".", end="")
        time.sleep(0.5)
    print(" connected:", wlan.ifconfig()[0])

def connect_mqtt():
    client = MQTTClient("quad-switch", secrets.MQTT_BROKER, port=secrets.MQTT_PORT)
    client.connect()
    print("Connected to MQTT broker:", secrets.MQTT_BROKER)
    return client

toggle_status(True)
connect_wifi()
mqtt = connect_mqtt()
mqtt.publish("homeassistant/device/quad-switch/status", b"online")
toggle_status(False)
print("Ready — press any button")

prev = [1, 1, 1, 1]

while True:
    for i, btn in enumerate(buttons):
        state = btn.value()
        if state != prev[i]:
            any_pressed = any(b.value() == 0 for b in buttons)
            for led in leds:
                led.value(1 if any_pressed else 0)
            if state == 0:
                topic = MQTT_TOPIC.format(i)
                try:
                    mqtt.publish(topic, b"pressed")
                    print(f"Button {i} → {topic}")
                except Exception as e:
                    print("MQTT error:", e)
                    toggle_status(True)
                    mqtt = connect_mqtt()
                    toggle_status(False)
            prev[i] = state
    time.sleep_ms(10)
