import serial.tools.list_ports
import serial
from hooks.Hook import *


class Serial(Hook):
    def __init__(self) -> None:
        if Serial.getPort() != None:
            self.ser = serial.Serial(port=Serial.getPort(), baudrate=115200)
        self.mess = ""

    def start(self):
        # if Serial.getPort() != None:
        #     self.ser = serial.Serial(port=Serial.getPort(), baudrate=115200)

        if self.ser.isOpen():
            print("Serial is open")
        else:
            print("Serial is not open")

    def getPort():
        ports = serial.tools.list_ports.comports()
        N = len(ports)
        commPort = "None"
        for i in range(0, N):
            port = ports[i]
            strPort = str(port)
            # print(strPort)
            if "USB-SERIAL" in strPort:
                splitPort = strPort.split(" ")
                commPort = splitPort[0]
        print(commPort)
        return commPort
    
    def processData(client , data):
        data = data.replace("!", "")
        data = data.replace("#", "")
        splitData = data.split(":")
        print(splitData)
        if splitData[0] == "TEMP":
            print("submitting ...")
            client.publish("phudang882/feeds/sensor2", splitData[1])
        # if splitData[0] == "LIGHT":
        #     print("submitting ...")
        #     client.publish("xMysT/feeds/light", splitData[1])
        if splitData[2] == "HUMI":
            print("submitting ...")
            client.publish("phudang882/feeds/sensor1", splitData[3])
        # if splitData[0] == "AI":
        #     print("submitting ...")
        #     client.publish("xMysT/feeds/ai", splitData[1])

    def readSerial(self, client):
        # print("I'm in")
        bytesToRead = self.ser.inWaiting()
        # print(self.ser)
        # print(bytesToRead, 'bs')
        if bytesToRead > 0:
            # global mess
            self.mess = self.mess + self.ser.read(bytesToRead).decode("UTF-8")
            while ("#" in self.mess) and ("!" in self.mess):
                start = self.mess.find("!")
                end = self.mess.find("#")
                Serial.processData(client, self.mess[start : end + 1])
                if end == len(self.mess):
                    self.mess = ""
                else:
                    self.mess = self.mess[end + 1 :]

    def on_message(self, feed, payload):
        print("Serial: Received: " + payload.decode() + ", feed_id: " + feed)
        # TODO: Send to serial
        if 'buttonA' in feed:
            print("Sent to serial: " + payload.decode())
            if payload.decode() == 'ON':
                self.ser.write('1'.encode())
            elif payload.decode() == 'OFF':
                self.ser.write('0'.encode())

        if 'buttonB' in feed:
            print("Sent to serial: " + payload.decode())
            if payload.decode() == 'ON':
                self.ser.write('3'.encode())
            elif payload.decode() == 'OFF':
                self.ser.write('2'.encode())
        # elif 'button2' in feed:
        #     print("Sent to serial: " + payload.decode())
        #     self.ser.write(str(payload).encode())



        
