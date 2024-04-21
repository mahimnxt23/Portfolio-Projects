# this one is for scripting purpose only!

from PyPDF2 import PdfReader
from pyttsx3 import init
import pdfplumber as pdp

file_to_convert = 'sample.pdf'

pdf_object = open(file_to_convert, mode='rb')  # making everything in readable binary format...
pdf_reader = PdfReader(pdf_object)
num_of_pages = len(pdf_reader.pages)  # knowing total pages available...


with pdp.open(file_to_convert) as pdf:

    for index in range(num_of_pages):
        page = pdf.pages[index]
        text = page.extract_text()  # extracting texts from the pdf page on current index...
        print(text)

        speaker = init()  # initializing pytts speaker engine...
        speech_rate = speaker.getProperty('rate')
        voice_property = speaker.getProperty('voices')

        speaker.setProperty('rate', 275)
        # speaker.setProperty('voice', voice_property[0].id)  # for male voice...
        speaker.setProperty('voice', voice_property[1].id)  # for female voice...

        speaker.say(text)  # making it say while reading...
        speaker.runAndWait()  # holding it till everything is narrated...
