from bluepy import btle
import numpy as np
import pyqtgraph as pg
from collections import deque
from PyQt5 import QtWidgets, QtCore
from pyqtgraph import PlotWidget, plot
import time

class MyDelegate(btle.DefaultDelegate):
    def __init__(self):
        btle.DefaultDelegate.__init__(self)
        self.times = deque([0], maxlen=100)
        self.vals = deque([0], maxlen=100)
        # self.counter = 0

    def handleNotification(self, cHandle, data):
        # ... perhaps check cHandle
        # ... process 'data'
        y = int(data.decode("utf-8"))
        self.vals.append(y)
        self.times.append(time.time())
        # print("handleNotification: " + str(cHandle) + " " + str(y))
    
class MainWindow(QtWidgets.QMainWindow):
    def __init__(self,deleg, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        self.graphWidget = pg.PlotWidget()
        self.setCentralWidget(self.graphWidget)
        self.delegate = deleg
        self.graphWidget.setBackground('w')
        pen = pg.mkPen(color=(255, 0, 0))
        self.data_line =  self.graphWidget.plot(self.delegate.times, self.delegate.vals, pen=pen)
        self.timer = QtCore.QTimer()
        self.timer.setInterval(10)
        self.timer.timeout.connect(self.update_plot_data)
        self.timer.start()
    def update_plot_data(self):
        # read new charac value
        # self.delegate.handleNotification(0,0)
        dev.waitForNotifications(0.1)
        self.data_line.setData(self.delegate.times, self.delegate.vals)  # Update the data.
        
        
    
def signal_handler(sig, frame):
    print('You pressed Ctrl+C!')
    dev.disconnect()
    exit(0)

MAC = "24:0A:C4:C0:6E:42"
SERVICE_UUID = "4fafc201-1fb5-459e-8fcc-c5c9c331914b"
CHARACTERISTIC_UUID = "beb5483e-36e1-4688-b7f5-ea07361b26a8"

# register the notification handler
the_delegate = MyDelegate()
dev = btle.Peripheral(MAC)
dev.setDelegate(the_delegate)

service_uuid = btle.UUID(SERVICE_UUID)
service = dev.getServiceByUUID(service_uuid)

# get the characteristic you want
ch = service.getCharacteristics(CHARACTERISTIC_UUID)[0]

# enable notifications
# dev.writeCharacteristic(ch.valHandle + 1, b"\x01\x00")

# start the Qt App
app = QtWidgets.QApplication([])
w = MainWindow(the_delegate)
w.show()
app.exec_()
# dev.disconnect()s
while True:
    # if dev.waitForNotifications(1.0):
        # handleNotification() was called
        # continue
    # print("Waiting...")
    pass