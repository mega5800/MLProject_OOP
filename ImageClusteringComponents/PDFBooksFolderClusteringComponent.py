class PDFBooksFolderClusteringComponent:
    def __init__(self, i_PDFBooksFolderPath):
        self.__m_PDFBooksFolderPath = i_PDFBooksFolderPath
        self.__m_ThreadManager = ThreadManager()
        self.__m_PDFBookClusteringComponentList = []

    def StartImageClusteringOnPDFBooksFolder(self):
        pdfBooksInPDFBooksFolderCounter = len(glob.glob(self.__m_PDFBooksFolderPath + "/*/")) + 1

        for currentPDFBookIndex in range(1, pdfBooksInPDFBooksFolderCounter):
            currentPDFBookPath = self.__m_PDFBooksFolderPath + r"\book{0}".format(currentPDFBookIndex)
            self.__m_ThreadManager.AddNewThreadToThreadsList(threading.Thread(target=self.__addNewPDFBookClusteringComponentToPDFBookClusteringComponentList, args=(currentPDFBookPath,)))

        self.__m_ThreadManager.PerformJoinFunctionOnThreadsList()

    def __addNewPDFBookClusteringComponentToPDFBookClusteringComponentList(self, i_PDFBookPath):
        self.__m_PDFBookClusteringComponentList.append(PDFBookClusteringComponent(i_PDFBookPath))


import glob
import threading
from Utilities.ThreadManager import ThreadManager
from ImageClusteringComponents.PDFBookClusteringComponent import PDFBookClusteringComponent
