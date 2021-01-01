import cv2
import numpy as np

class Page:
    __k_Threshold = 500
    __k_MaxLineGap = 350
    __k_MinLineLength = 1400
    __k_LineWidth = 115

    def __init__(self, i_PageNum, i_PageFolderPath, i_PageFilePath):
        self.__m_PageNum = i_PageNum
        self.__m_PageFolderPath = i_PageFolderPath
        self.__m_PageFilePath = i_PageFilePath
        self.__convertAndCropPNGFileToGrayScale()
        self.__preformCannyAndHoughLinesPOnImage()
        self.__sortImage()
        self.__cropLinesFromPage()

    def __convertAndCropPNGFileToGrayScale(self):
        imgToCropAndConvert = cv2.imread(self.__m_PageFilePath)
        imgToCropAndConvert = cv2.cvtColor(imgToCropAndConvert, cv2.COLOR_BGR2GRAY)
        imgToCropAndConvert = imgToCropAndConvert[835:3870, 0:2979]
        self.__m_PageImage = imgToCropAndConvert
        cv2.imwrite(self.__m_PageFilePath, imgToCropAndConvert)

    def __preformCannyAndHoughLinesPOnImage(self):
        self.__m_PageImage = cv2.Canny(self.__m_PageImage, 30, 11, apertureSize=3)
        self.__m_PageImage = cv2.HoughLinesP(self.__m_PageImage, 1, np.pi / 180, Page.__k_Threshold,
                                             maxLineGap=Page.__k_MaxLineGap, minLineLength=Page.__k_MinLineLength)

    def __sortImage(self):
        self.__m_PageImage = sorted(self.__m_PageImage, key=lambda x: x[:][0][1])

    def __cropLinesFromPage(self):
        self.__m_LinesList = []
        self.__m_yIndexList = []

        for line in self.__m_PageImage:
            if line[0][1] == line[0][3]:
                yIndex = line[0][1]
                if self.__distinctLineCheck(yIndex):
                    self.__m_yIndexList.append(yIndex)
                    cropLine(yIndex, textPagesList[i], i)

    def __distinctLineCheck(self, i_NumToCheck):
        result = True

        if len(self.__m_yIndexList) != 0:
            for lineYIndex in self.__m_yIndexList:
                if abs(i_NumToCheck - lineYIndex) < Page.__k_LineWidth / 2:
                    result = False
                    break

        return result
