class PDFBooksFolder:
    def __init__(self, i_PDFBooksFolderPath):
        self.__m_PDFBooksFolderPath = i_PDFBooksFolderPath
        self.__fillPDFBooksList()

    def __fillPDFBooksList(self):
        self.__m_PDFBooksList = []
        self.__m_PDFFilesInFolderCounter = len(glob.glob1(self.__m_PDFBooksFolderPath, "*.pdf"))

        for i in range(0, self.__m_PDFFilesInFolderCounter):  # should every file has it's own thread?
            currentPDFBookFolderPath = self.__m_PDFBooksFolderPath + "/book{0}".format(i + 1)
            currentPDFBookFilePath = self.__m_PDFBooksFolderPath + "/book{0}.pdf".format(i + 1)
            self.__m_PDFBooksList.append(PDFBook(i + 1, currentPDFBookFolderPath, currentPDFBookFilePath))


import glob
from Classes.PDFBook import PDFBook
