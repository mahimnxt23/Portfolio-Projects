from tkinter import Tk, filedialog, Scrollbar, Text, Button, END
from PyPDF2 import PdfReader
from pyttsx3 import init
import pdfplumber as pdp

text_i_am_reading = ''


def get_file():
    file = filedialog.askopenfilename(filetypes=[('PDF files', '*.pdf')])
    return file


def read_from_file():
    global text_i_am_reading
    desired_file = get_file()

    pdf_object = open(desired_file, mode='rb')  # making everything in readable binary format...
    pdf_reader = PdfReader(pdf_object)
    num_of_pages = len(pdf_reader.pages)  # knowing total pages available...

    with pdp.open(desired_file) as pdf:
        for index in range(num_of_pages):
            page = pdf.pages[index]
            text = page.extract_text()  # extracting texts from the pdf page on current index...

            text_i_am_reading += f'{text}\n\n'

    print(text_i_am_reading)
    text_box.insert(END, text_i_am_reading)


def speak_text():
    speaker = init()  # initializing pytts speaker engine...
    # speech_rate = speaker.getProperty('rate')
    # voice_property = speaker.getProperty('voices')

    # print(speech_rate)
    speaker.setProperty('rate', 250)
    # speaker.setProperty('voice', voice_property[0].id)  # for male voice...
    # speaker.setProperty('voice', voice_property[1].id)  # for female voice...

    speaker.say(text_i_am_reading)  # making it say while reading...
    speaker.runAndWait()  # holding it till everything is narrated...


window = Tk()
window.title('PDF to AudioBook')
window.minsize(width=720, height=430)
window.maxsize(width=720, height=430)
window.config(padx=20, pady=20)

scrollbar = Scrollbar(window, orient='vertical', jump=True)
scrollbar.pack(side='right', fill='y')

text_box = Text(window, font=('consolas', 14, 'normal'), width=50, height=15, highlightthickness=2, padx=5, pady=5,
                wrap='w', yscrollcommand=scrollbar.set)
text_box.pack()

open_button = Button(window, text='Choose PDF File', command=read_from_file)
open_button.pack(side='left', pady=10)

narrate_button = Button(window, text='Narrate it', command=speak_text)
narrate_button.pack(side='right', pady=10)


window.mainloop()
