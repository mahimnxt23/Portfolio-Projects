from tkinter import filedialog
from PyPDF2 import PdfReader
from pyttsx3 import init
import pdfplumber as pdp


def get_file():
    file = filedialog.askopenfilename(filetypes=[('PDF files', '*.pdf')])
    return file


def read_from_file():
    desired_file = get_file()

    pdf_object = open(desired_file, mode='rb')  # making everything in readable binary format...
    pdf_reader = PdfReader(pdf_object)
    num_of_pages = len(pdf_reader.pages)  # knowing total pages available...

    with pdp.open(desired_file) as pdf:
        for index in range(num_of_pages):
            page = pdf.pages[index]
            text = page.extract_text()  # extracting texts from the pdf page on current index...
            print(text)


