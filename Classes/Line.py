import cv2

from Croppers.WordCropper import WordCropper

class Line:
    def __init__(self, i_LineNum, i_LineFolderPath, i_LineFilePath):
        self.__m_NumberOfWordsInLine = 0
        self.__m_LineNum = i_LineNum
        self.__m_LineFolderPath = i_LineFolderPath
        self.__m_LineFilePath = i_LineFilePath
        self.__m_LineImage = cv2.imread(self.__m_LineFilePath)
        #self.__m_WordCropper = WordCropper(self.__m_LineImage, self.__m_LineFolderPath)
        #self.__m_WordsList = self.__m_WordCropper.GetWordsList()
