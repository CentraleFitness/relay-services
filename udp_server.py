import socket
import time
UDP_IP = '127.0.1.1'
UDP_PORT = 5544

sock = socket.socket(socket.AF_INET,
                     socket.SOCK_DGRAM)
try:
    sock.bind((UDP_IP, UDP_PORT))
    print('socket binded')

    while True:
        data, addr = sock.recv(1024)
        print(data)
        time.sleep(0.1)

except KeyboardInterrupt:
    print('stop')
