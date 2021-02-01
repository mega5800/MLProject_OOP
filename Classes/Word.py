class Word:
    def __init__(self, i_WordNum, i_WordFolderPath, i_WordFilePath):
        self.__m_WordNum = i_WordNum
        self.__m_WordFolderPath = i_WordFolderPath
        self.__m_WordFilePath = i_WordFilePath
        self.__m_WordImage = cv2.imread(self.__m_WordFilePath)
        self.__m_WordCropper = CropperFactory.CreateCropper(eCropperFactoryContext.CreateLetterCropper, self.__m_WordImage, self.__m_WordFolderPath)
        self.__m_WordsList = self.__m_WordCropper.GetItemsList()


import cv2
from Enums.eCropperFactoryContext import eCropperFactoryContext
from Croppers.CropperFactory import CropperFactory
