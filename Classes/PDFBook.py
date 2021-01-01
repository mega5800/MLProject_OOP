import os
import fitz
import cv2

from Classes.Page import Page

class PDFBook:
    __s_ZoomParam = 5

    def __init__(self, i_BookFilePath):
        self.__m_BookFilePath = i_BookFilePath
        self.__savePDFBookPagesAsPNGFiles()
        self.__savePNGFilesInPagesList()

    def __savePDFBookPagesAsPNGFiles(self):
        if not os.path.isdir("Pages"):  # make unique path for every book
            os.mkdir("Pages")

        doc = fitz.open(self.__m_BookFilePath)
        mat = fitz.Matrix(self.__s_ZoomParam, self.__s_ZoomParam)

        self.__m_NumberOfPagesInPDFBook = doc.pageCount
        for i in range(0, self.__m_NumberOfPagesInPDFBook):
            page = doc.loadPage(i)  # number of page
            pix = page.getPixmap(matrix=mat)
            output = "Pages/page{0}.png".format(i + 1)
            pix.writePNG(output)

    def __savePNGFilesInPagesList(self):
        self.__m_PagesList = []
        for i in range(0, self.__m_NumberOfPagesInPDFBook):
            tempImage = cv2.imread("Pages/page{0}.png".format(i + 1))
            self.__m_PagesList.append(Page(tempImage))
