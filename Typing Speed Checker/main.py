from tkinter import *
from words import *
import ctypes
import random

ctypes.windll.shcore.SetProcessDpiAwareness(1)  # for setting the screen sharper...


# UI setup...
window = Tk()
window.title('Typing Speed Tester')
window.minsize(width=640, height=360)

# using 'consolas' font for Labels and Buttons...
window.option_add(pattern='*Label.Font', value='consolas 30')
window.option_add(pattern='*Button.Font', value='consolas 30')


# helper functions...
def key_press(event=None):
    try:
        if event.char == label_right.cget('text')[0]:

            label_right.configure(text=label_right.cget('text')[1:])  # deleting 1 letter from the left side...
            label_left.configure(text=label_left.cget('text') + event.char)  # deleting 1 letter from the right side...
            current_letter_label.configure(text=label_right.cget('text')[0])  # popping the next letter to type...

    except TclError:
        pass


# noinspection PyGlobalUndefined
def start_timer():
    global seconds_passed

    # start timer ASAP!...
    seconds_passed += 1
    time_running_label.configure(text=f'{seconds_passed} Seconds')

    if writeable:
        window.after(1000, start_timer)  # this function calls itself until 1 minute expires...


# noinspection PyGlobalUndefined
def stop_the_test():
    global writeable, result_label, result_button
    writeable = False

    # calculating the word amount...
    word_amount = len(label_left.cget('text').split(' '))

    # destroying all trash widgets...
    time_running_label.destroy()
    current_letter_label.destroy()
    label_left.destroy()
    label_right.destroy()

    # display the test results...
    result_label = Label(window, text=f'Words per minute (WPM): {word_amount}', fg='black')
    result_label.place(relx=0.5, rely=0.4, anchor=CENTER)

    # display a 'restart game' button...
    result_button = Button(window, text='Retry', command=restart_test)
    result_button.place(relx=0.5, rely=0.6, anchor=CENTER)


def restart_test():
    # destroy all widgets related to results...
    result_label.destroy()
    result_button.destroy()

    # restart everything...
    writing_test_start()


# noinspection PyGlobalUndefined
# main function here...
def writing_test_start():
    global label_left, label_right, current_letter_label, time_running_label, writeable, seconds_passed

    words = random.choice(possible_texts)
    seconds_passed = 0
    split_point = 0  # current word and next word separator...

    # text which user has to typed...
    label_left = Label(window, text=words[0: split_point], fg='grey')
    label_left.place(relx=0.5, rely=0.5, anchor=E)  # 0.5 means it stays in center, E means East...

    # text which the user will type...
    label_right = Label(window, text=words[split_point:])
    label_right.place(relx=0.5, rely=0.5, anchor=W)  # W means West...

    # text which the user has to type...
    current_letter_label = Label(window, text=words[split_point], fg='grey')
    current_letter_label.place(relx=0.5, rely=0.6, anchor=N)  # N means North...

    # time which is left for the user...
    time_running_label = Label(window, text=f'0 Seconds', fg='grey')
    time_running_label.place(relx=0.5, rely=0.4, anchor=S)  # S means South...

    # switching writeable to True...
    writeable = True
    window.bind('<Key>', key_press)

    # binding callbacks to functions after specified time...
    window.after(60000, stop_the_test)
    window.after(1000, start_timer)


writing_test_start()  # starting the test game...

window.mainloop()  # keeping the window up and running all the time...
