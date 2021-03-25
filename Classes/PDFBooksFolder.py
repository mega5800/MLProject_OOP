class PDFBooksFolder:
    def __init__(self, i_PDFBooksFolderPath):
        self.__m_PDFBooksFolderPath = i_PDFBooksFolderPath

    def StartImageProcessingOnPDFBook(self):
        self.__m_PDFBooksList = []
        self.__m_ThreadsList = []
        self.__m_PDFFilesInFolderCounter = len(glob.glob1(self.__m_PDFBooksFolderPath, "*.pdf"))

        for i in range(0, self.__m_PDFFilesInFolderCounter):  # should every file has it's own thread?
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
import threading
from Classes.PDFBook import PDFBook
