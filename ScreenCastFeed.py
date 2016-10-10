import cv2
import numpy as np
import pyscreenshot as ImageGrab

class ScreenCastFeed:
    def __init__(self, name="sc"):
        self.name = name

    def get_frame(self):
        img = ImageGrab.grab()
    	img_np = np.array(img)
        print img_np.size
    	return img_np

    def set_frame(self, img_np):
    	frame = cv2.cvtColor(img_np, cv2.COLOR_BGR2GRAY)
    	cv2.imshow("test", frame)
    	cv2.waitKey(0)

if __name__=="__main__":
    sc = ScreenCastFeed("test")
    arr = sc.get_frame()
    sc.set_frame(arr)
