import paho.mqtt.client as mqtt
from random import randrange, uniform
import time

mqttBroker = "x22e12be.ala.us-east-1.emqxsl.com"
client = mqtt.Client("Temperature_Inside")
client.connect(mqttBroker)

while True:
    randNumber = uniform(20.0, 21.0)
    client.publish("TEMPERATURE", randNumber)
    print("Just published " + str(randNumber) + " to Topic TEMPERATURE")
    time.sleep(5)