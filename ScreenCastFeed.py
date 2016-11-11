import cv2
import numpy as np
import pyscreenshot as ImageGrab
import io
import sys
from PIL import Image, ImageTk
import Tkinter as tk


class ScreenCastFeed:
    def __init__(self, name="sc"):
        self.name = name

    def get_frame(self):
        img = ImageGrab.grab()
    	img_np = np.array(img)

        frame = cv2.cvtColor(img_np, cv2.COLOR_RGB2BGR)
        pil_im = Image.fromarray(frame)
        b = io.BytesIO()
        pil_im.save(b, 'jpeg')
        im_bytes = b.getvalue()
        return im_bytes

    def set_frame(self, frame_bytes):
	root = tk.Tk()
	screen_width = root.winfo_screenwidth()
	screen_height = root.winfo_screenheight()
	pil_bytes = io.BytesIO(frame_bytes)
        pil_image = Image.open(pil_bytes)
        photo = ImageTk.PhotoImage(image = pil_image)
	label = tk.Label(root, image= photo)
	label.place(x=0, y=0, relwidth= screen_width/2, relheight= screen_height/2)
	label.grid()
	root.mainloop()
	

if __name__=="__main__":
    sc = ScreenCastFeed("test")
    arr = sc.get_frame()
    sc.set_frame(arr)
