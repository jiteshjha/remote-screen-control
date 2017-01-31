import socket
import cv2
import numpy as np
import os
import time
import pyautogui 
from PIL import Image
import pyscreenshot as ImageGrab
import io

port = 10100
msg = socket.gethostbyname(socket.gethostname())
dest = ('<broadcast>',port)
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
s.sendto(msg, dest)
print msg
s.close()
TCP_IP = ''
TCP_IP_2 = ''
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
s.bind((TCP_IP_2,port))
message, address = s.recvfrom(1024)            
ad = ''.join(str(address));
ad1 = ad.split()
ad2= ad1[0]
ad3=ad2[2:15]
ad3 = ad3.replace("'", "")
ad3 = ad3.replace(",", "")
TCP_IP_2 = str(ad3)
TCP_IP = message
#print TCP_IP_2
print TCP_IP
s.close()
time.sleep(1)

TCP_IP =TCP_IP.strip()


#TCP_IP = '127.0.0.1'
TCP_PORT = 5006
MESSAGE = "Hello, World!"

TCP_PORT_2 = 9656
TCP_PORT_3 = 6969

s2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s2.connect((TCP_IP, TCP_PORT_3))



s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((TCP_IP, TCP_PORT))

s1 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s1.connect((TCP_IP, TCP_PORT_2))

screen_width, screen_height = pyautogui.size()
wsent = 0
hsent = 0
heightstr = str(screen_height).zfill(8)
widthstr = str(screen_width).zfill(8)

while hsent < 8:
	sent = s2.send(heightstr[hsent:])
	if sent == 0:
		raise RuntimeError("Socket connection broken")
	hsent += sent
while wsent < 8:
	sent = s2.send(widthstr[wsent:])
	if sent == 0:
		raise RuntimeError("Socket connection broken")
	wsent += sent


s2.close()

pid = os.fork()
if pid!=0:
   
    while 1:
	try:
        	img = ImageGrab.grab()
    		img_np = np.array(img)
        	frame = cv2.cvtColor(img_np, cv2.COLOR_RGB2BGR)
        	pil_im = Image.fromarray(frame)
        	b = io.BytesIO()
        	pil_im.save(b, 'jpeg')
        	im_bytes = b.getvalue()
        
        	totalsent = 0
        	metasent = 0
		length =len(im_bytes)
		lengthstr=str(length).zfill(8)

		while metasent < 8 :
		    sent = s.send(lengthstr[metasent:])
		    if sent == 0:
		        raise RuntimeError("Socket connection broken")
		    metasent += sent


		while totalsent < length :
		    sent = s.send(im_bytes[totalsent:])
		    if sent == 0:
		        raise RuntimeError("Socket connection broken")
		    totalsent += sent
	except Exception as e:
		print ("Error is: ", e)
else:
	child = pid
	while True:
		try:	    
			type = s1.recv(2)
			type = int(type)
			if type == 1:
				x = s1.recv(4)
				x = int(x)
				y = s1.recv(4)
				y = int(y)
				pyautogui.moveTo(x,y)
				pyautogui.click()
			if type == 2:
				x = s1.recv(4)
				x = int(x)
				y = s1.recv(4)
				y = int(y)
				pyautogui.moveTo(x,y)
				pyautogui.click(button='right')  
			if type == 0:
				x = s1.recv(20)
				if x == 'BackSpace':
					pyautogui.press('backspace')
				elif x == 'Delete':
					pyautogui.press('delete')
				elif x == 'Return':
					pyautogui.press('enter')
				elif x == 'Tab':
					pyautogui.press('tab')
				elif x == 'Control_L':
					pyautogui.press('ctrlleft')
				elif x == 'Control_R':
					pyautogui.press('ctrlright')
				elif x == 'Alt_L':
					pyautogui.press('altleft')
				elif x == 'Alt_R':
					pyautogui.press('altright')				
				elif x == 'Shift_L':
					pyautogui.press('shiftleft')
				elif x == 'Shift_R':
					pyautogui.press('shiftright')
				elif x == 'Escape':
					pyautogui.press('esc')
				elif x == 'space':
					pyautogui.press(' ')
				elif x == 'Up':
					pyautogui.press('up')
				elif x == 'Down':
					pyautogui.press('down')
				elif x == 'Right':
					pyautogui.press('right')
				elif x == 'Left':
					pyautogui.press('left')
				elif x == 'period':
					pyautogui.press('.')
				elif x == 'apostrophe':
					pyautogui.press('"')
				elif x == 'Term':
					pyautogui.hotkey('ctrl', 'alt', 't')
				else:
					pyautogui.press(x)
			if type == 3:
				farray = []
				fsize = s1.recv(3)
				fs = int(fsize)
				print fs
				filename = s1.recv(fs)
				print filename
				filename = filename.strip()				
				meta = s1.recv(8)
				print meta
				m = int(meta)
				print m
				mrec = 0
				while mrec < m:
					chunk = s1.recv(m - mrec)
					if chunk == b'':
						raise RuntimeError("Socket connection broken")
					farray.append(chunk)
					mrec +=  len(chunk)
				f = ''.join(farray)
				f2 = open(filename, 'wb').write(f)
			if type == 4:
				s.close()
				s1.close()
				os.system("kill "+ str(child))
				sys.exit()				
	
		except Exception as a:
			time.sleep(2)
			print ("Error is: ", a)        
s.close()
s1.close()
