import cv2

from Croppers.LineCropper import LineCropper

class Page:
    def __init__(self, i_PageNum, i_PageFolderPath, i_PageFilePath):
        self.__m_PageNum = i_PageNum
        self.__m_PageFolderPath = i_PageFolderPath
        self.__m_PageFilePath = i_PageFilePath
        self.__convertPNGFileToGrayScale()
        self.__m_LineCropper = LineCropper(self.__m_PageImage, self.__m_PageFolderPath)
        self.__m_LinesList = self.__m_LineCropper.GetLinesList()

    def __convertPNGFileToGrayScale(self):
        imgToConvert = cv2.imread(self.__m_PageFilePath)
        imgToConvert = cv2.cvtColor(imgToConvert, cv2.COLOR_BGR2GRAY)
        self.__m_PageImage = imgToConvert
        cv2.imwrite(self.__m_PageFilePath, imgToConvert)
