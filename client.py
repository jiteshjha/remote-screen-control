import socket
from ScreenCastFeed import ScreenCastFeed
import time

TCP_IP = '127.0.0.1'
#TCP_IP = '192.168.43.33'
TCP_PORT = 5005
BUFFER_SIZE = 4000000
MESSAGE = "Hello, World!"

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((TCP_IP, TCP_PORT))

sc = ScreenCastFeed("test")
while 1:
    arr = sc.get_frame()
    s.send(arr)
s.close()
