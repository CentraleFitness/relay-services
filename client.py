import socket
import sys

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.sendto(bytes(" ".join(sys.argv[1:]), "utf-8"), ("127.0.1.1", 4000))
