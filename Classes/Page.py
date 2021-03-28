class Page:
    def __init__(self, i_PageNum, i_PageFolderPath, i_PageFilePath):
        self.__m_PageNum = i_PageNum
        self.__m_PageFolderPath = i_PageFolderPath
        self.__m_PageFilePath = i_PageFilePath
        self.__m_PageImage = Utils.ConvertPNGFileToGrayScale(self.__m_PageFilePath)
        self.__m_LineCropper = CropperFactory.CreateCropper(eCropperFactoryContext.CreateLineCropper, self.__m_PageImage, self.__m_PageFolderPath)
        self.__m_LinesList = self.__m_LineCropper.GetItemsList()

from Utilities.Utils import Utils
from Enums.eCropperFactoryContext import eCropperFactoryContext
from Croppers.CropperFactory import CropperFactory
