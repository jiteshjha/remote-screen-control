import socket
from ScreenCastFeed import ScreenCastFeed

TCP_IP = '127.0.0.1'
TCP_PORT = 5005
BUFFER_SIZE = 4000000

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((TCP_IP, TCP_PORT))
s.listen(5)

conn, addr = s.accept()
print 'Connection address:', addr
sc = ScreenCastFeed("test")
while 1:
    print "server"
    data = conn.recv(BUFFER_SIZE)
    if not data: break
    sc.set_frame(data)
conn.close()
