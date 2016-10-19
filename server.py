import socket
from ScreenCastFeed import ScreenCastFeed
import pyxhook
import time
import os
TCP_IP = '127.0.0.1'
TCP_PORT = 5005
BUFFER_SIZE = 4000000

def kbevent( event ):
    
    print event
    
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((TCP_IP, TCP_PORT))
s.listen(5)

conn, addr = s.accept()
print 'Connection address:', addr
sc = ScreenCastFeed("test")

# Use bjoin instead of join when playing over LAN ;)
# Use join instead of bjoin when playing over Localhost :3
pid = os.fork()
if pid != 0:
    while 1:

        totrec=0
        metarec=0
        msgArray = []
        metaArray = []
        while metarec < 8:
            chunk = conn.recv(8 - metarec)
            if chunk == '':
                raise RuntimeError("Socket connection broken")
            metaArray.append(chunk)
            metarec += len(chunk)
        lengthstr= ''.join(metaArray)
        length=int(lengthstr)

        while totrec<length :
            chunk = conn.recv(length - totrec)
            if chunk == '':
                raise RuntimeError("Socket connection broken")
            msgArray.append(chunk)
            totrec += len(chunk)
        msgArray = ''.join(msgArray)
        sc.set_frame(msgArray)
    conn.close()
else:
    hookman = pyxhook.HookManager()
    #Define our callback to fire when a key is pressed down
    hookman.KeyDown = kbevent
    #Hook the keyboard
    hookman.HookKeyboard()
    #Start our listener
    hookman.start()
        
    #Create a loop to keep the application running
    running = True
    while running:
        time.sleep(0.1)
        
    #Close the listener when we are done
    hookman.cancel()

