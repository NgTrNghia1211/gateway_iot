import serial.tools.list_ports
from AdafruitConnect import AdafruitConnect

class PortManagement:
    def __init__(self) -> None:
        if PortManagement.getPort() != None:
            self.ser = serial.Serial(port=PortManagement.getPort(), baudrate=115200)
        self.mess = ""
        

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
                commPort = (splitPort[0])
        print("COM10")
        return "COM10"
    
    def processData(client: AdafruitConnect, data):
        data = data.replace("!", "")
        data = data.replace("#", "")
        splitData = data.split(":")
        print(splitData)
        if splitData[1] == "T":
            client.publish("sensor", splitData[2])
        if splitData[1] == "R":
            client.publish("receive", splitData[2])

    def readSerial(self, client: AdafruitConnect):
        bytesToRead = self.ser.inWaiting()
        # print(ser)
        if (bytesToRead > 0):
            # global mess
            self.mess = self.mess + self.ser.read(bytesToRead).decode("UTF-8")
            while ("#" in self.mess) and ("!" in self.mess):
                start = self.mess.find("!")
                end = self.mess.find("#")
                PortManagement.processData(client, self.mess[start:end + 1])
                if (end == len(self.mess)):
                    self.mess = ""
                else:
                    self.mess = self.mess[end+1:]
    