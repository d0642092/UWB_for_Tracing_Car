'''
將東西送進去 socket
'''
from socket import *
import threading
import time

class Forward(threading.Thread):
    def __init__(self, name, flag):
        threading.Thread.__init__(self)
        self.name = name
        self.flag = flag
        # self.time = time
    def run(self):
        HOST = '127.0.0.1'  # socket  server端的ip 可在內網
        PORT = 55688  # 'SendCommand.py'是你的server端
        ADDR = (HOST, PORT)
        BUFFSIZE = 1024
        i = 0
        client = socket(AF_INET, SOCK_STREAM)
        try:
            client.connect(ADDR)
            client.sendall(b'\xFA\x01\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFB\x0D\x0A')
            print("Server: ", client.recv(BUFFSIZE))
            print("Waiting...")
            while self.flag:
                pass
            client.sendall(b'\xFA\x08\x00\x00\x00\x00\x00\x00\x00\xFB\x0D\x0A')
            print("Server: ", client.recv(BUFFSIZE))
            client.close()
        except Exception:
            print("Please run SendCommand first")
            self.flag = False
