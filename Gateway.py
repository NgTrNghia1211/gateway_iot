from hooks.InfluxDB_Hook import *
from hooks.Adafruit_Hook import *
from hooks.Serial_Hook import *
import paho.mqtt.client as mqtt
import time
import os

# read from conf.ini
import configparser

broker_address = "io.adafruit.com"
port = 1883
# username = os.getenv("ADA_USR")
# password = os.getenv("ADA_KEY")

AIO_FEED_IDS = ["button1", "button2"]


class Gateway:
    def __init__(self):
        self.config = configparser.ConfigParser()
        try:
            self.config.read(os.path.join(os.path.dirname(__file__), 'conf.ini'))
        except Exception as e:
            print(e)
            print("Failed to read config file")
            exit(1)

        self.hooks: list[Hook] = []
        self.username = self.config["DEFAULT"]["ADA_USR"]
        self.password = self.config["DEFAULT"]["ADA_KEY"]
        self.feeds = self.config["DEFAULT"]["ADA_FDS"].split(",")
        self.client = mqtt.Client(
            clean_session=True,
        )
        self.client.username_pw_set(
            username=self.username,
            password=self.password,
        )
        try:
            self.client.connect(broker_address, port)
            for feed in self.feeds:
                self.client.subscribe(self.username + "/feeds/" + feed)
        except Exception as e:
            print(e)
            print("Failed to connect to broker")

        self.client.on_message = self.on_message
        self.client.on_subscribe = self.on_subscribe

    def addHook(self, hook: Hook):
        try:
            self.hooks.append(hook)
        except Exception as e:
            print(e)
            print("Failed to add hook")

    def start(self):
        for hook in self.hooks:
            try:
                hook.start()
            except Exception as e:
                print(e)
                print("Failed to start hook")

        self.client.loop_start()

    def stop(self):
        self.client.loop_stop()

    def on_message(self, client, userdata, message):
        print("Received message: " + str(message.payload.decode("utf-8")))
        for hook in self.hooks:
            hook.on_message(message.topic, message.payload)

    def on_subscribe(self, client, userdata, mid, granted_qos):
        print("Subscribed: " + str(mid) + " " + str(granted_qos))
