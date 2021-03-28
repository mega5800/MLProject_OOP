class PDFBooksFolderClusteringComponent:
    def __init__(self, i_PDFBooksFolderPath, i_CategoriesNumber=40):
        self.__m_PDFBooksFolderPath = i_PDFBooksFolderPath
        self.__m_CategoriesNumber = i_CategoriesNumber
        self.__m_ThreadManager = ThreadManager()
        self.__m_PDFBookClusteringComponentList = []

    def StartImageClusteringOnPDFBooksFolder(self):
        pdfBooksInPDFBooksFolderCounter = len(glob.glob(self.__m_PDFBooksFolderPath + "/*/")) + 1

        for currentPDFBookIndex in range(1, pdfBooksInPDFBooksFolderCounter):
            currentPDFBookPath = self.__m_PDFBooksFolderPath + r"\book{0}".format(currentPDFBookIndex)
            self.__m_ThreadManager.AddNewThreadToThreadsList(threading.Thread(target=self.__addNewPDFBookClusteringComponentToPDFBookClusteringComponentList, args=(currentPDFBookPath,)))

        self.__m_ThreadManager.PerformJoinFunctionOnThreadsList()

    def __addNewPDFBookClusteringComponentToPDFBookClusteringComponentList(self, i_PDFBookPath):
        self.__m_PDFBookClusteringComponentList.append(PDFBookClusteringComponent(i_PDFBookPath, self.__m_CategoriesNumber))


import glob
import threading
from Classes.ThreadManager import ThreadManager
from Classes.PDFBookClusteringComponent import PDFBookClusteringComponent
