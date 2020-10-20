from sensors import *
import socket
import traceback
import sys
import numpy as np
import time


class ReadRoutine(object):
    __instance = None

    def __new__(cls):

        if ReadRoutine.__instance is None:
            total_s = 6
            ReadRoutine.__instance = object.__new__(cls)
            ReadRoutine.__instance.sensors = Sensors(Sensors.MAX_X)
            ReadRoutine.__instance.cycle_past = 0
            ReadRoutine.__instance.n_s = 6
            ReadRoutine.__instance.active_sensors = [False]*total_s
            ReadRoutine.__instance.sensor_pos = []
            ReadRoutine.__instance.FRTC = 32768.0
            ReadRoutine.__instance.sock = None

        return ReadRoutine.__instance

    def read_values(self):

        data = self.sock.recv(Sensors.WINDOWS_SIZE)
        while (len(data) != Sensors.WINDOWS_SIZE):
            data += self.sock.recv(Sensors.WINDOWS_SIZE-len(data))
        start = time.time()
        self.sensors.appendFromWindow(data)

    def connect(self, dest):
        # print("connecting...")
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        self.sock.connect(dest)

    def start(self):
        self.sock.send("start".encode())

    def close(self):
        self.sock.close()


def main():
    print(1)
    HOST = '192.168.1.108'     # Endereco IP do Servidor
    PORT = 8001            # Porta que o Servidor esta
    ReadRoutine().connect((HOST, PORT))
    ReadRoutine().start()

    while True:
        try:

            ReadRoutine().read_values()
            print(list(np.diff(ReadRoutine().sensors.rtc)))

        except Exception as e:
            exc_type, exc_value, exc_traceback = sys.exc_info()
            print("*** print_tb:")
            traceback.print_tb(exc_traceback, limit=1, file=sys.stdout)
            print("*** print_exception:")
            traceback.print_exception(exc_type, exc_value, exc_traceback,
                                      limit=2, file=sys.stdout)

            sock.close()
            break


if __name__ == "__main__":
    main()
