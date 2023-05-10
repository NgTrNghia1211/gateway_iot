from hooks.Hook import Hook
# from Gateway import Gateway
import Adafruit_IO
# import paho.mqtt.client as mqtt



class Adafruit(Hook):
    def __init__(self, username, key, feed_ids):
        self.username = username
        self.key = key
        self.feed_ids = feed_ids
        self.client = None

    def start(self):
        self.client = Adafruit_IO.Client(self.username, self.key)
        self.client.on_message = self.on_message

        for feed in self.feed_ids:
            self.client.subscribe(feed)

    def on_message(self, feed, payload):
        print("Received: " + payload + ", feed_id: " + feed)
        #self.client.publish(feed, payload)
    

    def on_subscribe(self, feed):
        print("Subscribed to: " + feed)
