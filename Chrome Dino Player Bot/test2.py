import pyautogui as gui
import keyboard
# from time import sleep


while True:
    img = gui.screenshot()
    screen = img.getpixel(xy=(290, 180))
    
    # press q to exit the robot
    if keyboard.is_pressed("q"):
        break

    gui.screenshot().save("dino.jpg")
    gui.click(100, 100)
