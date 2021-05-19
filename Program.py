import sys
from ImageClusteringComponents.PDFBooksFolderClusteringComponent import PDFBooksFolderClusteringComponent
from Classes.PDFBooksFolder import PDFBooksFolder
from Utilities.Utils import Utils
import time

constErrorMessage = "An exception occurred\nPlease check the PDF books folder path"

def performAMethodInTryCatchBlock(i_MethodPointer, i_ErrorMessage):
    try:
        start = time.time()
        i_MethodPointer()
        end = time.time()
        print("\nElapsed time = {}\n".format(end - start))
    except:
        print(i_ErrorMessage)
    finally:
        Utils.PlayFinishSound()


if len(sys.argv) > 1:
    pdfBooksFolderPath = sys.argv[1]
    pdfBooksFolder = PDFBooksFolder(pdfBooksFolderPath)
    performAMethodInTryCatchBlock(pdfBooksFolder.StartImageProcessingOnPDFBooksFolder, constErrorMessage)
    pdfBooksFolderClusteringComponent = PDFBooksFolderClusteringComponent(pdfBooksFolderPath)
    performAMethodInTryCatchBlock(pdfBooksFolderClusteringComponent.StartImageClusteringOnPDFBooksFolder, constErrorMessage)
else:
    print("Please enter a pdf books folder path")
