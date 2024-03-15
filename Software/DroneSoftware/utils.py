import requests
from threading import Thread
import urllib.request

def check_internet_conn():
    try:
        urllib.request.urlopen('http://google.com') 
        return True
    except:
        return False

def displayPrintLine(text, duration=0.5):

    body = {
        "text": text,
        "duration": duration
    }

    url = 'http://127.0.0.1:5001/printLine'

    request = lambda url, body: requests.post(url=url, json=body)

    thread = Thread(target=request, args=(url, body))
    thread.start()

import time

def periodicTask(payload, frequency):
    
    assert frequency != 0
    sleep_time = 1 / frequency

    while True:
        payload()
        time.sleep(sleep_time)

import random
from paho.mqtt import client as mqtt_client

class MQTTSubscriber():
    broker = 'x22e12be.ala.us-east-1.emqxsl.com'
    port = 8883
    username = '8299164486'
    password = 'Acrazt1956##'

    def __init__(self, on_message, topics=set(['cmd'])):

        self.client_id = f'python-mqtt-{random.randint(0, 1000)}'
        self.is_connected = False
        self.topics = topics
        self.client = mqtt_client.Client(self.client_id)
        self.on_message = on_message
        # Set CA certificate
        self.client.tls_set(ca_certs='/home/acrazt/Desktop/AI-Drone-Wall-E/Software/DroneSoftware/emqxsl-ca.crt') 
        self.client.username_pw_set(self.username, self.password)
        
    def on_connect(self, client, userdata, flags, rc):

        print(f'On connect! rc: {rc}')
        if rc == 0:
            displayPrintLine("MQTT Broker! OK")
            self.is_connected = True
        else:
            displayPrintLine(f"MQTT Broker! ERROR {rc}", 3)
    
    def on_disconnect(self, client, userdata, flags, rc):
        print('On disconnect!')
        displayPrintLine('MQTT Disconnected!', 0.2)
        self.is_connected = False

    def connect(self):
        try:
            self.client.on_connect = self.on_connect
            self.client.on_disconnect = self.on_disconnect
            displayPrintLine("Connecting to MQTT Broker!")
            self.client.connect(self.broker, self.port)

            for topic in self.topics:
                self.subscribe(topic)

            self.client.on_message = self.on_message

        except Exception as e:
            displayPrintLine(str(e))
    
    def start(self):
        self.client.loop_forever()
        #self.client.loop_start()

    def isConnected(self):
        return self.is_connected

    def subscribe(self,topic):
        print(f'Subscribe to {topic}')
        self.topics.add(topic)
        self.client.subscribe(topic)

    def publish(self, topic, msg, retain=False):
        result = self.client.publish(topic=topic, payload=msg, retain=retain)
        status = result[0]
        self.is_connected = status == 0
        if status == 0:
            return True
        else:
            self.connect()
            return self.is_connected


from pymavlink import mavutil

def check_fc(port='/dev/serial/by-id/usb-FTDI_FT232R_USB_UART_A400f3WS-if00-port0'):
    source_system = 255
    baudrate = 57600
    force_connected = False
    
    try:
        the_connection = mavutil.mavlink_connection(port, autoreconnect=True,
                                        source_system=source_system,
                                        baud=baudrate,
                                        force_connected=force_connected)

        if the_connection.wait_heartbeat(timeout=1) == None:
            displayPrintLine("ERROR: FC has no Heartbeat!")
            the_connection.close()
            return False
        else:
            displayPrintLine('Connected to FC!')
            the_connection.close()
            return True

    except Exception as e:
        print(e)
        displayPrintLine(str(e), 3)
        return False