from bluepy import btle
# import bytearray
import time
import matplotlib.pyplot as plt
import signal
import numpy as np

MAC = "24:0A:C4:C0:6E:42"
SERVICE_UUID = "4fafc201-1fb5-459e-8fcc-c5c9c331914b"
CHARACTERISTIC_UUID = "beb5483e-36e1-4688-b7f5-ea07361b26a8"

print("Connect to:" + MAC)
dev = btle.Peripheral(MAC)

print("\n--- dev ----------------------------")
print(type(dev))
print(dev)

print("\n--- dev.services -------------------")
for svc in dev.services:
    print(str(svc))
    
print("\n------------------------------------")
print("Get Serice By UUID: " + SERVICE_UUID)
service_uuid = btle.UUID(SERVICE_UUID)
service = dev.getServiceByUUID(service_uuid)

print(service)
print("\n--- service.getCharacteristics() ---")
print(type(service.getCharacteristics()))
print(service.getCharacteristics())

#----------------------------------------------
characteristics = dev.getCharacteristics()
print("\n--- dev.getCharacteristics() -------")
print(type(characteristics))
print(characteristics)

def signal_handler(sig, frame):
    print('You pressed Ctrl+C!')
    dev.disconnect()
    exit(0)

class MyDelegate(btle.DefaultDelegate):
    def __init__(self):
        btle.DefaultDelegate.__init__(self)
        # ... initialise here
        self.vals = []
        self.last = 0
        self.times = []
        self.it = 0

    def handleNotification(self, cHandle, data):
        # ... perhaps check cHandle
        # ... process 'data'
        y = int(data.decode("utf-8"))
        # print("handleNotification: " + str(cHandle) + " " + str(y))
        if self.last !=y:
            self.it +=1
            self.last = -1
            self.vals.append(y)
            self.times.append(time.time())
            if len(self.vals) > 50:
                self.vals.pop(0)
                self.times.pop(0)
                # plt.cla()
            plt.cla()
            plt.plot(self.times, self.vals, 'r-')
            # plt.plot(time.time(), y, 'ro')
            # remove the first point from the plot
            plt.pause(0.01)

# register the notification handler
dev.setDelegate(MyDelegate())

# for char in characteristics:
#     print("----------")
#     print(type(char))
#     print(char)
#     print(char.uuid)
#     if(char.uuid == CHARACTERISTIC_UUID ):
#         print("=== !CHARACTERISTIC_UUID matched! ==")
#         print(char)
#         print(dir(char))
#         print(char.getDescriptors)
#         print(char.propNames)
#         print(char.properties)
#         print(type(char.read()))
#         print(char.read())
plt.ion()
# register signal handler
signal.signal(signal.SIGINT, signal_handler)
while True:
    if dev.waitForNotifications(1.0):
        # handleNotification() was called
        continue
    pass
            # time.sleep(3)

    
#print("=== dev ============================")
#print(dir(dev))
#print("=== service ========================")
#print(dir(service))