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
BORDER = '#3C2C3E'
FG = 'khaki'
BG = '#4B5D67'

FONT_FAMILY1 = 'Calibri'
FONT_FAMILY2 = 'Helvetica'

FONT_SIZE1 = 14
FONT_SIZE2 = 18
FONT_SIZE3 = 24

FONT_STYLE1 = 'normal'
FONT_STYLE2 = 'italic'
FONT_STYLE3 = 'bold'

PARA_FONT = (FONT_FAMILY1, FONT_SIZE1, FONT_STYLE3)
PARA_FONT2 = (FONT_FAMILY1, 12, FONT_STYLE2)
HEAD_FONT = (FONT_FAMILY2, FONT_SIZE3, FONT_STYLE1)

heading = 'CONSIDER WRITING WITH MAGICAL INK'
instruction = 'If you don\'t press any key for 5 seconds, the text you have written will disappear'
# - - - - - - - - - - - - - - - - - - - - - - - - - STYLING - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -


# UI setup...
window = Tk()
window.title('Text Disappearing App')
window.minsize(width=640, height=360)
window.configure(bg=BG, padx=20, pady=10)

# using 'consolas' font for Labels and Buttons...
window.option_add(pattern='*Label.Font', value='consolas 30')
window.option_add(pattern='*Button.Font', value='consolas 30')

heading_label = Label(text=heading, font=HEAD_FONT, bg=BG, fg=FG, padx=10, pady=10)
instruction_label = Label(text=instruction, font=PARA_FONT2, bg=BG, fg=FG, pady=10)

typing_area = Text(font=PARA_FONT, bg=BG, fg=FG, width=100, height=15, wrap='w', highlightcolor=BORDER,
                   highlightthickness=4, highlightbackground=BORDER, padx=5, pady=5)
typing_area.bind('<KeyPress>', start_calculating)

reset_button = Button(text='Reset Everything!', fg=FG, bg=BG, font=PARA_FONT, border=3, highlightbackground=FG,
                      highlightcolor=FG, highlightthickness=0, width=50, command=reset_app)
save_button = Button(text='Save!', fg=FG, bg=BG, font=PARA_FONT, border=3, highlightbackground=FG, width=50,
                     highlightcolor=FG, highlightthickness=0, command=save_text)

heading_label.grid(row=0, column=0, columnspan=3)
instruction_label.grid(row=2, column=0, columnspan=3)
typing_area.grid(row=3, column=0, columnspan=3)
reset_button.grid(row=4, column=0)
save_button.grid(row=4, column=2)


window.mainloop()
