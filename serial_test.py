import os
from re import T
import serial
import time
from collections import deque

class recv_data:
    def __init__(self):
        print('waiting')
        while True:
            if os.path.exists('/dev/rfcomm0'):
                self.comport = serial.Serial('/dev/rfcomm0', 9600, timeout=2)
                break
            else:
                continue
        print('connect')

    def read_data(self):
        q_data = deque()
        recv = self.comport.readline()
        num = recv.decode('ascii')
        count = 0
        print(num)
        while num != '':
            if count == int(num):
                break
            print(count)
            recv = self.comport.readline()
            dir = recv.decode('ascii').rstrip()
            recv = self.comport.readline()
            dis = recv.decode('ascii').rstrip()
            print('data', dir, dis)
            data = [int(dir), int(dis)]
            q_data.append(data)
            count = count + 1

        return q_data, num

    def port_close(self):
        self.comport.close()

    def get_data(self):
        q, num = self.read_data()
        return q, num