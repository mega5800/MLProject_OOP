import winsound

from Classes.PDFBooksFolder import PDFBooksFolder

book = PDFBooksFolder("pdf books")
frequency = 2500
duration = 500
winsound.Beep(frequency, duration)
