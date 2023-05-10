import time
import os
from Gateway import *
from hooks.InfluxDB_Hook import *
from hooks.Adafruit_Hook import *
from hooks.Serial_Hook import *
# from hooks.Masking_Hook import *

model = 'keras_model.h5'
class_names = 'labels.txt'


gateway = Gateway()
# ai = AiDetector(model, class_names)
# gateway.addHook(ai)

serial = Serial()
gateway.addHook(serial)

influx = InfluxDB(
    host=gateway.config["INFLUXDB"]["INF_URL"],
    bucket=gateway.config["INFLUXDB"]["INF_BUCKET"],
    org=gateway.config["INFLUXDB"]["INF_ORG"],
    token=gateway.config["INFLUXDB"]["INF_TOKEN"],
)
# gateway.addHook(influx)

# adafruit = Adafruit()
# gateway.addHook(adafruit)

def main():
    # counter_ai = 5
    gateway.start()
    while True:
        # counter_ai = counter_ai - 1
        # if counter_ai <= 0:
        #     counter_ai = 5
        #     Serial.processData(gateway.client, ai.masking_detector())
        serial.readSerial(gateway.client)
        time.sleep(1)


if __name__ == "__main__":
    main()
