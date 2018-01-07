import socket
import time
import sys
import pickle

UDP_IP = sys.argv[1]
UDP_PORT = int(sys.argv[2])

sock = socket.socket(socket.AF_INET,
                     socket.SOCK_DGRAM)
try:
    sock.bind((UDP_IP, UDP_PORT))
    print('socket binded')

    while True:
        data, addr = sock.recvfrom(1024)
        print(data)

except KeyboardInterrupt:
    print('stop')
