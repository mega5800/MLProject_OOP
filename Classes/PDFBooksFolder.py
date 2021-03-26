class PDFBooksFolder:
    def __init__(self, i_PDFBooksFolderPath):
        self.__m_PDFBooksFolderPath = i_PDFBooksFolderPath
        self.__renameFilesInPDFBooksFolderPath()

    def __renameFilesInPDFBooksFolderPath(self):
        pdfFilesList = glob.glob1(self.__m_PDFBooksFolderPath, "*.pdf")
        self.__m_PDFFilesInFolderCounter = len(pdfFilesList)

        for i in range(0, self.__m_PDFFilesInFolderCounter):
            oldFilePath = self.__m_PDFBooksFolderPath + "/{}".format(pdfFilesList[i])
            os.rename(oldFilePath, self.__m_PDFBooksFolderPath + "/book{0}.pdf".format(i + 1))

    def StartImageProcessingOnPDFBook(self):
        self.__m_PDFBooksList = []
        self.__m_ThreadsList = []

        for i in range(0, self.__m_PDFFilesInFolderCounter):
            currentPDFBookFolderPath = self.__m_PDFBooksFolderPath + r"\book{0}".format(i + 1)
            currentPDFBookFilePath = self.__m_PDFBooksFolderPath + r"\book{0}.pdf".format(i + 1)
            self.__m_ThreadsList.append(threading.Thread(target=self.__addNewPDFBookObjectToPDFBooksList, args=(i + 1, currentPDFBookFolderPath, currentPDFBookFilePath,)))
            self.__m_ThreadsList[i].start()

        self.__performJoinFunctionOnThreadsList()

    def __addNewPDFBookObjectToPDFBooksList(self, i_Counter, i_CurrentPDFBookFolderPath, i_CurrentPDFBookFilePath):
        self.__m_PDFBooksList.append(PDFBook(i_Counter, i_CurrentPDFBookFolderPath, i_CurrentPDFBookFilePath))

    def __performJoinFunctionOnThreadsList(self):
        for thread in self.__m_ThreadsList:
            thread.join()

import glob
import os
import threading
from Classes.PDFBook import PDFBook
