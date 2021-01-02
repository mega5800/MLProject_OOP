import cv2
import numpy as np
import os

class Page:
    __k_Threshold = 350
    __k_MaxLineGap = 250
    __k_MinLineLength = 550
    __k_LineWidth = 115

    def __init__(self, i_PageNum, i_PageFolderPath, i_PageFilePath):
        self.__m_NumberOfLinesInPage = 0
        self.__m_PageNum = i_PageNum
        self.__m_PageFolderPath = i_PageFolderPath
        self.__m_PageFilePath = i_PageFilePath
        self.__convertAndCropPNGFileToGrayScale()
        self.__preformCannyAndHoughLinesPOnImage()
        self.__sortProcessedPageImage()
        self.__cropLinesFromPage()

        self.__dynamicLineMarks()

    def __convertAndCropPNGFileToGrayScale(self):
        imgToCropAndConvert = cv2.imread(self.__m_PageFilePath)
        imgToCropAndConvert = cv2.cvtColor(imgToCropAndConvert, cv2.COLOR_BGR2GRAY)
        imgToCropAndConvert = imgToCropAndConvert[850:3830, 0:2979]
        self.__m_PageImage = imgToCropAndConvert
        cv2.imwrite(self.__m_PageFilePath, imgToCropAndConvert)

    def __preformCannyAndHoughLinesPOnImage(self):
        self.__m_ProcessedPageImage = cv2.Canny(self.__m_PageImage, 30, 11, apertureSize=3)
        self.__m_ProcessedPageImage = cv2.HoughLinesP(self.__m_ProcessedPageImage, 1, np.pi / 180, Page.__k_Threshold, maxLineGap=Page.__k_MaxLineGap, minLineLength=Page.__k_MinLineLength)

    def __sortProcessedPageImage(self):
        self.__m_ProcessedPageImage = sorted(self.__m_ProcessedPageImage, key=lambda x: x[:][0][1])

    def __cropLinesFromPage(self):
        self.__m_LinesList = []
        self.__m_yIndexList = []

        for line in self.__m_ProcessedPageImage:
            if line[0][1] == line[0][3]:
                yIndex = line[0][1]
                if self.__distinctLineCheck(yIndex):
                    self.__m_yIndexList.append(yIndex)
                    self.__cropNewLine(yIndex)

    def __distinctLineCheck(self, i_NumToCheck):
        result = True

        if len(self.__m_yIndexList) != 0:
            for lineYIndex in self.__m_yIndexList:
                if abs(i_NumToCheck - lineYIndex) < Page.__k_LineWidth / 2:
                    result = False
                    break

        return result

    def __cropNewLine(self, i_YIndexToCrop):
        if i_YIndexToCrop - Page.__k_LineWidth < 0:
            lineImage = self.__m_PageImage[0:i_YIndexToCrop + 15, 0:3304]
        else:
            lineImage = self.__m_PageImage[i_YIndexToCrop - Page.__k_LineWidth+15:i_YIndexToCrop+25, 0:2979]

        if not os.path.isdir(self.__m_PageFolderPath):
            os.mkdir(self.__m_PageFolderPath)

        self.__m_NumberOfLinesInPage += 1
        lineFilePath = self.__m_PageFolderPath + "/line{0}.png".format(self.__m_NumberOfLinesInPage)
        cv2.imwrite(lineFilePath, lineImage)

    """
        if i_YIndexToCrop - k_LineWidth < 0:
            line_image = i_ImageToCrop[0:i_YIndexToCrop + 15, 0:3304]
        else:
            line_image = i_ImageToCrop[i_YIndexToCrop - k_LineWidth + 15:i_YIndexToCrop + 15, 0:3304]
    """

    def __dynamicLineMarks(self):
        imageCopy = self.__m_PageImage.copy()

        for line in self.__m_ProcessedPageImage:
            x1, y1, x2, y2 = line[0]
            if y1 == y2:
                cv2.line(imageCopy, (x1, y1), (x2, y2), (0, 255, 0), 3)
        fileName = self.__m_PageFolderPath + "/page{0}_Lines.png".format(self.__m_PageNum)
        cv2.imwrite(fileName, imageCopy)
