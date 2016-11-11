import socket
import pyxhook
import time
import os,sys
import PIL
import Tkinter as tk
import io
import cv2
from Tkinter import *
import numpy as np
from PIL import Image, ImageTk
import traceback


#TCP_IP = '192.168.43.46'
#TCP_IP = '127.0.0.1'
TCP_IP = ''
port = 10100
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
s.bind((TCP_IP,port))
message, address = s.recvfrom(10104)            
ad = ''.join(str(address));
ad1 = ad.split()
ad2= ad1[0]
ad3=ad2[2:15]
print ad3, message
#print ad, ad1, ad2, ad3
s.close()
ad3 = ad3.replace("'", "")
ad3 = ad3.replace(",", "")
TCP_IP = str(ad3)

#time.sleep(1)
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.connect(('8.8.8.8', 0))
msg = s.getsockname()[0]
TCP_IP = msg
print TCP_IP
dest = ('<broadcast>',10100)
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
s.sendto(TCP_IP, dest)
s.close()





TCP_PORT = 5006
BUFFER_SIZE = 10000000

TCP_PORT_2 = 9656
TCP_PORT_3 = 6969
def kbevent( event ):
    	type = 0
	conn1.send(str(type).zfill(2))  	
	conn1.send(event.Key)
    #print event
    
#def key(event):
#    print "pressed", repr(event.char)

def left(event):
	type = 1
	conn1.send(str(type).zfill(2))
	conn1.send(str(event.x).zfill(4))
	conn1.send(str(event.y).zfill(4))
	

#def middle(event):
#    print("M Single Click, Button-l", event.x, event.y) 

def right(event):
	type = 2
	conn1.send(str(type).zfill(2))
	conn1.send(str(event.x).zfill(4))
	conn1.send(str(event.y).zfill(4))

#def _resize_image(event):
#        origin = (0,0)
#        size = (event.width, event.height)
#        if label.bbox("bg") != origin + size:
#            self.delete("bg")
#            self.image = self.img_copy.resize(size)
#            self.background_image = ImageTk.PhotoImage(self.image)
#            self.create_image(*origin,anchor="nw",image=self.background_image,tags="bg")
#            self.tag_lower("bg","all")
		
#def scroll_up(event):
#   print("SU Single Click, Button-l", event.x, event.y)


#def scroll_down(event):
#    print("SD Single Click, Button-l", event.x, event.y)  

def quit(event):                           
    print("Double Click, so let's stop", repr(event)) 

s2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s2.bind((TCP_IP, TCP_PORT_3))
s2.listen(5)


s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((TCP_IP, TCP_PORT))
s.listen(5)

s1 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s1.bind((TCP_IP, TCP_PORT_2))
s1.listen(5)

conn2, addr2 = s2.accept()

hrec = 0
wrec = 0
harray = []
warray = []
while hrec < 8:
	chunk = conn2.recv(8 - hrec)
	if chunk == '':
		raise RuntimeError("Socket connection broken")
	harray.append(chunk)
	hrec +=  len(chunk)
heightstr = ''.join(harray)
screen_height = int(heightstr)
while wrec < 8:
	chunk = conn2.recv(8 - wrec)
	if chunk == '':
		raise RuntimeError("Socket connection broken")
	warray.append(chunk)
	wrec +=  len(chunk)
widthstr = ''.join(warray)
screen_width = int(widthstr)
conn2.close()

s2.close()

root = tk.Tk()
root.title("Harambe")
root.geometry(str(screen_width) + "x" + str(screen_height))

conn, addr = s.accept()
conn1, addr1 = s1.accept()
#print 'Connection address:', addr

#print 'KeyBoard Connection address:', addr1
		
# Use bjoin instead of join when playing over LAN ;)
# Use join instead of bjoin when playing over Localhost :3
counter = 0
pid = os.fork()
if pid != 0:
	while 1:
		try:
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
			pil_bytes = io.BytesIO(msgArray)
			pil_image = Image.open(pil_bytes)
			img_np = np.array(pil_image)
			frame = cv2.cvtColor(np.array(img_np), cv2.COLOR_BGR2RGB)
			pil_image = Image.fromarray(frame)
			#pil_image = pil_image.resize((screen_width/2,screen_height/2), PIL.Image.ANTIALIAS)
			photo = ImageTk.PhotoImage(image = pil_image)	
			if (counter == 0) :	
				label = tk.Label(root, image= photo)
				#label.pack()
				label.bind('<Button-1>', left)
 				#label.bind('<Button-2>', middle)
 				label.bind('<Button-3>', right)
				#label.bind("<Configure>",_resize_image)
 				#label.bind('<Button-4>', scroll_up)
 				#label.bind('<Button-5>', scroll_down)
				#label.bind("<Key>", key)
				label.grid()
				label.update()
			else:
				label.configure(image = photo)
				label.image = photo
				label.update()
			counter = counter + 1
		
	    		
		except Exception as a:
			print ("Error is: ", a)
	    	
    	conn.close()
	print "Close conn"
else:
	try:	    
	    print "Enter 0 to Specify new Line:"
	    
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
	except Exception as a:
		print "Error is: ", a
root.mainloop()

s1.close()
s.close()
