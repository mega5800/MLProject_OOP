import fitz
import threading
from Classes.Page import Page
from Classes.Utils import Utils
import os

class PDFBook:
    __k_ZoomParam = 5

    def __init__(self, i_PDFBookNum, i_PDFBookFolderPath, i_PDFBookFilePath):
        self.__m_PDFBookNum = i_PDFBookNum
        self.__m_PDFBookFolderPath = i_PDFBookFolderPath
        self.__m_PDFBookFilePath = i_PDFBookFilePath
        self.__savePDFBookPagesAsSeparatePNGFiles()
        self.__convertPNGFilesToPagesList()

    def __savePDFBookPagesAsSeparatePNGFiles(self):
        Utils.CreateFolder(self.__m_PDFBookFolderPath)
        doc = fitz.open(self.__m_PDFBookFilePath)
        mat = fitz.Matrix(self.__k_ZoomParam, self.__k_ZoomParam)
        self.__m_NumberOfPagesInPDFBook = doc.pageCount
        for i in range(0, self.__m_NumberOfPagesInPDFBook):
            page = doc.loadPage(i)
            pix = page.getPixmap(matrix=mat)
            output = self.__m_PDFBookFolderPath + "/page{0}.png".format(i + 1)
            pix.writePNG(output)

    def __convertPNGFilesToPagesList(self):
        self.__m_PagesList = []
        self.__m_ThreadsList = []

        for i in range(0, self.__m_NumberOfPagesInPDFBook):
            currentPageFolderPath = self.__m_PDFBookFolderPath + "/page{0}".format(i + 1)
            currentPageFilePath = self.__m_PDFBookFolderPath + "/page{0}.png".format(i + 1)
            self.__m_ThreadsList.append(threading.Thread(target=self.__addNewPageToPagesList, args=(i + 1, currentPageFolderPath, currentPageFilePath,)))
            self.__m_ThreadsList[i].start()

        self.__performJoinFunctionOnThreadsList()
        self.__deletePagesFiles()

    def __addNewPageToPagesList(self, i_Counter, i_CurrentPageFolderPath, i_CurrentPageFilePath):
        self.__m_PagesList.append(Page(i_Counter, i_CurrentPageFolderPath, i_CurrentPageFilePath))

    def __performJoinFunctionOnThreadsList(self):
        for thread in self.__m_ThreadsList:
            thread.join()

    def __deletePagesFiles(self):
        for i in range(0, self.__m_NumberOfPagesInPDFBook):
            currentPageFilePath = self.__m_PDFBookFolderPath + "/page{0}.png".format(i + 1)
            os.remove(currentPageFilePath)
