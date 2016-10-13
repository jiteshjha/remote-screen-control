import socket
from ScreenCastFeed import ScreenCastFeed
import time

TCP_IP = '127.0.0.1'
#TCP_IP = '192.168.43.33'
TCP_PORT = 5005
MESSAGE = "Hello, World!"

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((TCP_IP, TCP_PORT))

sc = ScreenCastFeed("test")
while 1:
    arr = sc.get_frame()
    # length =len(arr)
    # lengthstr=str(length).zfill(8)
    #
    # print length
    # print lengthstr
    # print "---"
    #
    # sent = s.send(arr)

    totalsent = 0
    metasent = 0
    length =len(arr)
    lengthstr=str(length).zfill(8)

    while metasent < 8 :
        sent = s.send(lengthstr[metasent:])
        if sent == 0:
            raise RuntimeError("Socket connection broken")
        metasent += sent


    while totalsent < length :
        sent = s.send(arr[totalsent:])
        if sent == 0:
            raise RuntimeError("Socket connection broken")
        totalsent += sent

s.close()
