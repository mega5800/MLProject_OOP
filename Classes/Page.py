import cv2
import numpy as np
import os

class Page:
    __k_KernelSize = 5
    __k_LowThreshold = 50
    __k_HighThreshold = 150
    __k_CannyThreshold = 312
    __k_MinLineLength = 750
    __k_MaxLineGap = 2000
    __k_LineWidth = 115

    def __init__(self, i_PageNum, i_PageFolderPath, i_PageFilePath):
        self.__m_NumberOfLinesInPage = 0
        self.__m_PageNum = i_PageNum
        self.__m_PageFolderPath = i_PageFolderPath
        self.__m_PageFilePath = i_PageFilePath

        self.__convertPNGFileToGrayScale()
        self.__preformHoughLinesPOnImage()
        self.__sortProcessedPageImage()
        self.__cropLinesFromPage()

    def __preformHoughLinesPOnImage(self):
        imgCopy = self.__m_PageImage.copy()
        blur_gray = cv2.GaussianBlur(imgCopy, (Page.__k_KernelSize, Page.__k_KernelSize), 0)
        edges = cv2.Canny(blur_gray, Page.__k_LowThreshold, Page.__k_HighThreshold)
        line_image = np.copy(imgCopy) * 0
        self.__m_ProcessedPageImage = cv2.HoughLinesP(edges, 1, np.pi / 180, Page.__k_CannyThreshold, np.array([]), Page.__k_MinLineLength, Page.__k_MaxLineGap)

        # testing actions
        for line in self.__m_ProcessedPageImage:
            for x1, y1, x2, y2 in line:
                cv2.line(line_image, (x1, y1), (x2, y2), (255, 0, 0), 5)

        if not os.path.isdir(self.__m_PageFolderPath):
            os.mkdir(self.__m_PageFolderPath)

        lines_edges = cv2.addWeighted(imgCopy, 0.8, line_image, 1, 0)
        cv2.imwrite(self.__m_PageFolderPath+"/lines_edges_test.png", lines_edges)

    def __convertPNGFileToGrayScale(self):
        imgToCropAndConvert = cv2.imread(self.__m_PageFilePath)
        imgToCropAndConvert = cv2.cvtColor(imgToCropAndConvert, cv2.COLOR_BGR2GRAY)
        self.__m_PageImage = imgToCropAndConvert
        cv2.imwrite(self.__m_PageFilePath, imgToCropAndConvert)

    def __sortProcessedPageImage(self):
        self.__m_ProcessedPageImage = sorted(self.__m_ProcessedPageImage, key=lambda x: x[:][0][1])

    def __cropLinesFromPage(self):
        #self.__m_LinesList = []
        self.__m_yIndexList = []

        for line in self.__m_ProcessedPageImage:
            if line[0][1] > 900 and line[0][1] == line[0][3]:
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
        lineImage = self.__m_PageImage[i_YIndexToCrop - Page.__k_LineWidth+15:i_YIndexToCrop+20, 0:4212]
        if not os.path.isdir(self.__m_PageFolderPath):
            os.mkdir(self.__m_PageFolderPath)

        self.__m_NumberOfLinesInPage += 1
        lineFilePath = self.__m_PageFolderPath + "/line{0}.png".format(self.__m_NumberOfLinesInPage)
        cv2.imwrite(lineFilePath, lineImage)
