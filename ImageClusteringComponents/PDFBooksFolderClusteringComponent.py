class PDFBooksFolderClusteringComponent:
    def __init__(self, i_PDFBooksFolderPath):
        self.__m_PDFBooksFolderPath = i_PDFBooksFolderPath
        self.__m_PDFBookClusteringComponentList = []

    def StartImageClusteringOnPDFBooksFolder(self):
        pdfBooksInPDFBooksFolderCounter = len(glob.glob(self.__m_PDFBooksFolderPath + "/*/")) + 1

        for currentPDFBookIndex in range(1, pdfBooksInPDFBooksFolderCounter):
            print("\nCurrent page is page {}".format(currentPDFBookIndex))
            currentPDFBookPath = self.__m_PDFBooksFolderPath + r"\book{0}".format(currentPDFBookIndex)
            self.__m_PDFBookClusteringComponentList.append(PDFBookClusteringComponent(currentPDFBookPath))


import glob
from ImageClusteringComponents.PDFBookClusteringComponent import PDFBookClusteringComponent
