import cv2
import numpy as np
import pyscreenshot as ImageGrab
import io
import sys
from PIL import Image

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
    	pil_bytes = io.BytesIO(frame_bytes)
        pil_image = Image.open(pil_bytes)
        cv_image = cv2.cvtColor(np.array(pil_image), cv2.COLOR_RGB2BGR)
        cv2.imshow("test", cv_image)
    	cv2.waitKey(10)

if __name__=="__main__":
    sc = ScreenCastFeed("test")
    arr = sc.get_frame()
    sc.set_frame(arr)
