import winsound
from Classes.PDFBooksFolder import PDFBooksFolder
import pybind11module

pybind11module.sayHello()
book = PDFBooksFolder("pdf books")
frequency = 2500
duration = 500
winsound.Beep(frequency, duration)
