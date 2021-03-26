import sys
import winsound
from Classes.ImageClusteringComponent import ImageClusteringComponent
from Classes.PDFBooksFolder import PDFBooksFolder

constErrorMessage = "An exception occurred\nPlease check the PDF books folder path"

def finishSound():
    frequency = 2500
    duration = 500
    winsound.Beep(frequency, duration)

def performAMethodInTryCatchBlock(i_MethodPointer, i_ErrorMessage):
    try:
        i_MethodPointer()
    except:
        print(i_ErrorMessage)


if len(sys.argv) > 1:
    pdfBooksFolderPath = sys.argv[1]
    pdfBooksFolder = PDFBooksFolder(pdfBooksFolderPath)
    performAMethodInTryCatchBlock(pdfBooksFolder.StartImageProcessingOnPDFBook, constErrorMessage)

    # maybe i should find another way to write this
    if len(sys.argv) == 3:
        imageClusteringComponent = ImageClusteringComponent(pdfBooksFolderPath, i_CategoriesNumber=sys.argv[2])
    else:
        imageClusteringComponent = ImageClusteringComponent(pdfBooksFolderPath)

    performAMethodInTryCatchBlock(imageClusteringComponent.StartImageClustering, constErrorMessage)
    finishSound()
else:
    print("Please enter a pdf books folder path")
