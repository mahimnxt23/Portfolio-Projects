import cv2
import numpy as np
import pyautogui as gui
from PIL import Image, ImageGrab
from time import sleep, time
from math import floor


def grab_screen(bbox=None):
    img = ImageGrab.grab(bbox=bbox)
    img = np.array(img)
    return cv2.cvtColor(img, cv2.COLOR_RGB2BGR)


while True:
    img = grab_screen()
    cv2.imshow('screen', img)
    cv2.waitKey(0)
