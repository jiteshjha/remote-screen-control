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
from tkFileDialog import askopenfilename

child = 0
new_width = 0
new_height = 0
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
#print ad3, message
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


#TCP_IP = '127.0.0.1'

TCP_PORT = 5006
BUFFER_SIZE = 10000000

TCP_PORT_2 = 9656
TCP_PORT_3 = 6969
def kbevent( event ):
    	type = 0
	conn1.send(str(type).zfill(2))  	
	conn1.send(event.Key)


def left(event):
	type = 1
	x = ((event.x))
	y = ((event.y))	
	conn1.send(str(type).zfill(2))
	conn1.send(str(event.x).zfill(4))
	conn1.send(str(event.y).zfill(4))
	


def right(event):
	type = 2
	x = ((event.x))
	y = ((event.y))
	conn1.send(str(type).zfill(2))
	conn1.send(str(x).zfill(4))
	conn1.send(str(y).zfill(4))

def _resize_image(event):
        origin = (0,0)
        size = (event.width, event.height)
	if label.bbox("bg") != origin + size:
        	global new_height 
		new_height = event.height
		global new_width 
		new_width = event.width
		print new_width, new_height	

def sendHotKey():
	type = 0
	conn1.send(str(type).zfill(2))  	
	conn1.send("Term")	

def sendFile():
	try:
		Tk().withdraw()
		filename = askopenfilename()
		list = filename.split('/')
		l = len(list)
		filename = filename.replace(' ', '')
		type = 3
		conn1.send(str(type).zfill(2))		
		conn1.send(str(len(list[l-1])).zfill(3))
		print len(list[l-1])		
		conn1.send(str(list[l-1]))	
		f = open(filename, 'rb').read()
		meta = len(f)
		print f
		print meta
		conn1.send(str(meta).zfill(8))
		m = 0
		while m < meta :
			sent = conn1.send(f[m:])
			if sent == 0:
				raise RuntimeError("Socket connection broken")
			m += sent
		
	except Exception as a:
		print ("Error is: ", a)

def closeButton():
	type = 4
	conn1.send(str(type).zfill(2))
	conn1.close()
	conn2.close()
	s1.close()
	s.close()	
	root.destroy()
	os.system("kill "+str(child))
	sys.exit()


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

new_width = screen_width
new_height = screen_height

s2.close()
conn, addr = s.accept()
conn1, addr1 = s1.accept()

root = tk.Tk()
root.title("Harambe")
root.geometry(str(screen_width) + "x" + str(screen_height + 40))
#root.bind("<Configure>",_resize_image)
openTerm = tk.Button(root, text = "Open Terminal", padx = 10, pady = 10, justify = CENTER, command = sendHotKey)
openTerm.place(y = (new_height), x = (new_width - 400))   	
sendFile = tk.Button(root, text = "Send File", padx = 10, pady = 10, justify = CENTER, command = sendFile)
sendFile.place(y = (new_height), x = (400))   
closeB = tk.Button(root, text = "X", padx = 10, pady = 10, justify = CENTER, command = closeButton)
closeB.place(y = (new_height), x = 50)   


counter = 0
pid = os.fork()
if pid != 0:
	print "Starting: "
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
			pil_image = pil_image.resize((new_width,new_height), PIL.Image.ANTIALIAS)
			photo = ImageTk.PhotoImage(image = pil_image)	
			if (counter == 0) :	
				label = tk.Label(root, image= photo)
				label.bind('<Button-1>', left)
 				#label.bind('<Button-2>', middle)
 				label.bind('<Button-3>', right)
				#label.bind('<Button-4>', scroll_up)
 				#label.bind('<Button-5>', scroll_down)
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
	child = pid
	try:	    
	    
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
