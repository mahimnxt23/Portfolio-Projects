from tkinter import filedialog
from PyPDF2 import PdfReader
from pyttsx3 import init
import pdfplumber as pdp


def get_file():
    file = filedialog.askopenfilename(filetypes=[('PDF files', '*.pdf')])
    return file

