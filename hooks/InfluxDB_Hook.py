from hooks.Hook import *
import influxdb_client
from influxdb_client.client.write_api import SYNCHRONOUS
from influxdb_client.client.write_api import WriteOptions
from influxdb_client.client.write_api import WritePrecision
from influxdb_client.client.write_api import WriteApi

import os


class InfluxDB(Hook):
    def __init__(self, host: str, bucket: str, org: str, token: str) -> None:
        self.client = None
        self.host = host
        self.token = token
        self.org = org
        self.bucket = bucket
        self.write_api = None

    def start(self):
        print("Starting InfluxDB Hook")
        self.client = influxdb_client.InfluxDBClient(
            url=self.host, token=self.token, org=self.org
        )
        self.write_api = self.client.write_api(
            write_options=WriteOptions(
                batch_size=1000,
                flush_interval=10_000,
                jitter_interval=2_000,
                retry_interval=5_000,
                max_retries=5,
                max_retry_delay=30_000,
                exponential_base=2,
            )
        )
        print("InfluxDB Connected")

    def on_message(self, feed, payload):
        print("InfluxDB: Received: " + payload.decode() + ", feed_id: " + feed)
        #self.write(feed, float(payload))

    def on_subscribe(self, feed):
        print("Subscribed to: " + feed)

    def write(self, measurement: str, value: float):
        self.write_api.write(self.bucket, self.org, f"{measurement} value={value}")

    def close(self):
        self.client.close()
