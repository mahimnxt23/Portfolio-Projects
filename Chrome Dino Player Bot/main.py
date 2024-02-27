
# import pyautogui as gui
from PIL import ImageGrab
from time import sleep
import keyboard

x_start, x_end = (235, 350)


def smash_key(key):
    keyboard.press(key)


def is_colliding(pos):
    # bird triggering...
    for x in range(x_start, x_end):
        for y in range(320, 395):
            if pos[x, y] > 100:
                smash_key("down")
                # keyboard.press("down")
                sleep(0.2)
                keyboard.release("down")
                return

    # cactus triggering...
    for x in range(x_start, x_end):
        for y in range(440, 480):
            if pos[x, y] > 100:
                smash_key("up")
                return

    return


def start_bot():
    sleep(1)
    keyboard.press_and_release("space")
    # smash_key("space")

    while True:
        
        if keyboard.is_pressed('q'):
            break
            
        image = ImageGrab.grab().convert("L")
        data = image.load()
        is_colliding(data)


start_bot()
