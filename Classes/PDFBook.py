import os
import fitz

from Classes.Page import Page

class PDFBook:
    __s_ZoomParam = 5

    def __init__(self, i_PDFBookNum, i_PDFBookFolderPath, i_PDFBookFilePath):
        self.__m_PDFBookNum = i_PDFBookNum
        self.__m_PDFBookFolderPath = i_PDFBookFolderPath
        self.__m_PDFBookFilePath = i_PDFBookFilePath
        self.__savePDFBookPagesAsSeparatePNGFiles()
        self.__savePNGFilesInPagesList()

    def __savePDFBookPagesAsSeparatePNGFiles(self):
        if not os.path.isdir(self.__m_PDFBookFolderPath):
            os.mkdir(self.__m_PDFBookFolderPath)

        doc = fitz.open(self.__m_PDFBookFilePath)
        mat = fitz.Matrix(self.__s_ZoomParam, self.__s_ZoomParam)
        self.__m_NumberOfPagesInPDFBook = doc.pageCount
        for i in range(0, self.__m_NumberOfPagesInPDFBook):
            page = doc.loadPage(i)  # number of page
            pix = page.getPixmap(matrix=mat)
            output = self.__m_PDFBookFolderPath + "/page{0}.png".format(i + 1)
            pix.writePNG(output)

    def __savePNGFilesInPagesList(self):
        self.__m_PagesList = []
        
        for i in range(0, self.__m_NumberOfPagesInPDFBook):
            currentPageFolderPath = self.__m_PDFBookFolderPath + "/page{0}".format(i + 1)
            currentPageFilePath = self.__m_PDFBookFolderPath + "/page{0}.png".format(i + 1)
            self.__m_PagesList.append(Page(i+1, currentPageFolderPath, currentPageFilePath))
