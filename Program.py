import winsound
from Classes.ImageClusteringComponent import ImageClusteringComponent
from Classes.PDFBooksFolder import PDFBooksFolder


def finishSound():
    frequency = 2500
    duration = 500
    winsound.Beep(frequency, duration)


pdfBooksFolder = PDFBooksFolder(r"F:\Python Projects\MLProject_OOP\pdf books")
pdfBooksFolder.StartImageProcessingOnPDFBook()


#pythonImageClusteringComponent = ImageClusteringComponent(r"C:\Users\mega5\Desktop\python book1\book1")
#pythonImageClusteringComponent.StartImageClustering()
finishSound()
