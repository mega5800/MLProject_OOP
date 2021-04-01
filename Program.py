import sys
import winsound
from ImageClusteringComponents.PDFBooksFolderClusteringComponent import PDFBooksFolderClusteringComponent
from Classes.PDFBooksFolder import PDFBooksFolder
import time

constErrorMessage = "An exception occurred\nPlease check the PDF books folder path"

def finishSound():
    frequency = 2500
    duration = 500
    winsound.Beep(frequency, duration)

def performAMethodInTryCatchBlock(i_MethodPointer, i_ErrorMessage):
    try:
        # create own timer class
        start = time.time()
        i_MethodPointer()
        end = time.time()
        print("\nElapsed time = {}\n".format(end - start))
    except:
        print(i_ErrorMessage)
    finally:
        finishSound()


if len(sys.argv) > 1:
    pdfBooksFolderPath = sys.argv[1]
    pdfBooksFolder = PDFBooksFolder(pdfBooksFolderPath)
    performAMethodInTryCatchBlock(pdfBooksFolder.StartImageProcessingOnPDFBooksFolder, constErrorMessage)

    # maybe i should find another way to write this
    if len(sys.argv) == 3:
        categoriesNumber = int(sys.argv[2])
        pdfBooksFolderClusteringComponent = PDFBooksFolderClusteringComponent(pdfBooksFolderPath, i_CategoriesNumber=categoriesNumber)
    else:
        pdfBooksFolderClusteringComponent = PDFBooksFolderClusteringComponent(pdfBooksFolderPath)

    performAMethodInTryCatchBlock(pdfBooksFolderClusteringComponent.StartImageClusteringOnPDFBooksFolder, constErrorMessage)
else:
    print("Please enter a pdf books folder path")
