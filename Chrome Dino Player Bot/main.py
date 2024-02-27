import pyautogui as gui
from PIL import ImageGrab
from time import sleep
import keyboard

x_start, x_end = (215, 350)


def hit(key):
    gui.keyDown(key)


def is_colliding(pos):

    # cactus triggering...
    for x in range(x_start, x_end):
        for y in range(440, 480):
            if pos[x, y] > 100:
                hit("up")
                return True

    # bird triggering...
    for x in range(x_start, x_end):
        for y in range(320, 395):
            if pos[x, y] > 100:
                hit("down")
                sleep(0.2)
                keyboard.release('down')
                return True

    return False


if __name__ == "__main__":
    sleep(1)
    keyboard.press_and_release('space')

    while True:
        image = ImageGrab.grab().convert("L")
        data = image.load()
        is_colliding(data)
