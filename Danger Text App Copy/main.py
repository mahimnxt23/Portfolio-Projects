import ctypes
from tkinter import *


ctypes.windll.shcore.SetProcessDpiAwareness(1)  # for setting the screen sharper...


user_writen_texts = ''
timer = None


# helper functions stay here...
def start_calculating(event):  # as it listens at keypress...
    global timer, user_writen_texts

    if timer is not None:
        window.after_cancel(timer)
    if event.keysym == 'BackSpace':
        user_writen_texts = user_writen_texts[0: len(user_writen_texts) - 1]
    elif event.char:
        user_writen_texts += event.char
        timer = window.after(5000, reset_app)
    return


def reset_app():
    global timer, user_writen_texts

    typing_area.delete('1.0', 'end')
    user_writen_texts = ''
    timer = None
    return


def save_text():
    global user_writen_texts

    if user_writen_texts == '':
        return

    try:
        file = open('writen_text.txt', mode='r')

    except FileNotFoundError:
        file = open('writen_text.txt', mode='w')
        file.write(user_writen_texts)
        user_writen_texts = ''
        return

    else:
        content = file.read()
        if content == '':
            text_to_write = user_writen_texts
        else:
            text_to_write = f'\n{user_writen_texts}'

        with open('writen_text.txt', 'a') as file:
            file.write(text_to_write)
            user_writen_texts = ''

    finally:
        return


# - - - - - - - - - - - - - - - - - - - - - - - - - STYLING - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
BORDER = '#93B1A6'
FG = '#9EC8B9'
BG = '#030637'

FONT_FAMILY = 'consolas'

FONT_SIZE1 = 14
FONT_SIZE2 = 18
FONT_SIZE3 = 24

FONT_STYLE1 = 'normal'
FONT_STYLE2 = 'italic'
FONT_STYLE3 = 'bold'

BASE_FONT = (FONT_FAMILY, FONT_SIZE1, FONT_STYLE3)
INSTRUCTION_FONT = (FONT_FAMILY, 12, FONT_STYLE2)
HEADING_FONT = (FONT_FAMILY, FONT_SIZE3, FONT_STYLE1)

heading = 'CONSIDER WRITING WITH MAGICAL INK'
instruction = '( If you don\'t press any key for 5 seconds, the text you have written will disappear )'
# - - - - - - - - - - - - - - - - - - - - - - - - - STYLING - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -


# UI setup...
window = Tk()
window.title('Text Disappearing App')
window.minsize(width=1060, height=550)
window.maxsize(width=1060, height=550)
window.configure(bg=BG, padx=20, pady=20)


# labels...
heading_label = Label(text=heading, font=HEADING_FONT, bg=BG, fg=FG, padx=10, pady=10)
instruction_label = Label(text=instruction, font=INSTRUCTION_FONT, bg=BG, fg=FG, pady=10)

# text areas...
typing_area = Text(font=BASE_FONT, bg=BG, fg=FG, width=100, height=15, wrap='w', highlightcolor=BORDER,
                   highlightthickness=4, highlightbackground=BORDER, padx=5, pady=5)
typing_area.bind('<KeyPress>', start_calculating)

# buttons...
reset_button = Button(text='Reset Everything!', fg=FG, bg=BG, font=BASE_FONT, border=3, highlightbackground=FG,
                      highlightcolor=FG, highlightthickness=0, width=50, pady=5, command=reset_app)
save_button = Button(text='Save!', fg=FG, bg=BG, font=BASE_FONT, border=3, highlightbackground=FG, width=50,
                     highlightcolor=FG, highlightthickness=0, pady=5, command=save_text)


# UI placements...
heading_label.grid(row=0, column=0, columnspan=3)
instruction_label.grid(row=2, column=0, columnspan=3)
typing_area.grid(row=3, column=0, columnspan=3)
reset_button.grid(row=4, column=0)
save_button.grid(row=4, column=2)


window.mainloop()  # keeping the window on loop...
