import sys
import uuid
import threading
import time
from read_routine import *
from save_routine import *
from enum import Enum


from PyQt5 import QtWidgets
from INTERFACE_choose_app import Ui_MainWindow as ChooseAppWindow


class Status(Enum):
    STOP = 0
    WORKING = 1
    FINDPROBLEM = -1
    FINISHED = -2
    CONNECTING = 2


class WifiConnection:
    def __init__(self, name="ACELEROMETROS", port=0x1001):
        self.name = name
        self.sock = None
        self.port = port
        self.status = Status.STOP
        self.t = None

    def close(self, bluetooth_devices_window):
        bluetooth_devices_window.close()

    def __connect(self, addr):
        try:
            ReadRoutine().connect(addr)
        except:
            print("impossible to connect")
        try:
            ReadRoutine().start()
            self.status = Status.WORKING
        except:
            self.status = Status.FINISHED

        while True:
            try:

                ReadRoutine().read_values()
                SaveRoutine().save_routine()

            except KeyboardInterrupt:
                # print ("finalizando conexão...")
                ReadRoutine().close()
                self.status = Status.FINISHED
                return 1

        self.sock.close()
        return 0

    def wifiConnect(self, list_devices, ip, bluetooth_devices_window, home_window, screen_size):

        addr = (ip, 8001)

        self.t = threading.Thread(target=self.__connect, args=(addr,))
        self.t.start()
        self.close(bluetooth_devices_window)

        self.close(home_window)

        self.window = QtWidgets.QMainWindow()
        choose = ChooseAppWindow()
        choose.setupUi(self.window, screen_size)
        self.window.show()
        return 0
