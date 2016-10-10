import socket
from ScreenCastFeed import ScreenCastFeed

TCP_IP = '127.0.0.1'
TCP_PORT = 5005
BUFFER_SIZE = 4000000
MESSAGE = "Hello, World!"

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((TCP_IP, TCP_PORT))
sc = ScreenCastFeed("test")
arr = sc.get_frame()
print arr
s.send(arr)
s.close()
