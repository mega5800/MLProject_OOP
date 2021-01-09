class Line:
    def __init__(self, i_LineNum, i_LineFolderPath, i_LineFilePath):
        self.__m_LineNum = i_LineNum
        self.__m_LineFolderPath = i_LineFolderPath
        self.__m_LineFilePath = i_LineFilePath
        self.__m_LineImage = Utils.ConvertPNGFileToGrayScale(self.__m_LineFilePath)
        self.__m_WordCropper = CropperFactory.CreateCropper(eCropperFactoryContext.CreateWordCropper, self.__m_LineImage, self.__m_LineFolderPath)
        self.__m_WordsList = self.__m_WordCropper.GetItemsList()

from Classes.Utils import Utils
from Enums.eCropperFactoryContext import eCropperFactoryContext
from Croppers.CropperFactory import CropperFactory
