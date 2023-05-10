import  sys
from Adafruit_IO import MQTTClient


class AdafruitConnect:
        def __init__(self, username, key, feed_ids):
            self.username = username
            self.key = key
            self.feed_ids = feed_ids
            self.client = MQTTClient(self.username, self.key)

            self.client.on_message = self.message

        def connect(self):
            self.client.connect()

        def subscribe(self):
            for feed in self.feed_ids:
                self.client.subscribe(feed)

        def publish(self, feed, data):
            self.client.publish(feed, data)

        def message(client, feed, payload):
            print("Received: " + payload + ", feed_id: " + feed)

        def run(self):
            self.client.loop_background()
            
        
