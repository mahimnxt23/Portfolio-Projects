# import pyautogui as gui
from PIL import ImageGrab
# from time import sleep

x_start, x_end = (200, 275)


def take_screenshot():
    # sleep(1)
    
    image = ImageGrab.grab().convert('L')
    data = image.load()
    
    # cactus triggering...
    for x in range(x_start, x_end):
        for y in range(440, 480):
            data[x, y] = 0
    
    # bird triggering...
    for x in range((x_start - 50), (x_end - 50)):
        for y in range(320, 395):
            data[x, y] = 0
            
    # day/night theme detection...
    for x in range(x_start, (x_end - 25)):
        for y in range(130, 150):
            data[x, y] = 0
    
    image.show()


take_screenshot()
