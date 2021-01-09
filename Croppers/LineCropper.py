import cv2
import numpy as np
import os

# רעיון של רשת סטטיסטית
# נחשב את הערך התחתון עם הכי הרבה קולות וערך עליון עם הכי הרבה קולות
# ונתחשב רק בשורות בטווח הזה

from Classes.Line import Line
from Classes.Utils import Utils


class LineCropper:
    __k_KernelSize = 5
    __k_LowThreshold = 50
    __k_HighThreshold = 150
    __k_CannyThreshold = 300
    __k_MinLineLength = 750
    __k_MaxLineGap = 2000
    __k_LineWidth = 115

    def __init__(self, i_PageImage, i_PageImageFolderPath):
        self.__m_NumberOfLinesInPage = 0
        self.__m_PageImageToCrop = i_PageImage
        self.__m_PageImageToCropFolderPath = i_PageImageFolderPath

    def GetLinesList(self):
        tempNumpyArr = self.__preformHoughLinesPOnImage()
        self.__getNecessaryLines(tempNumpyArr)
        self.__sortProcessedPageImage()
        self.__cropLinesFromPage()
        self.__saveHoughLinesPResultImage()

        return self.__m_LinesList

    def __preformHoughLinesPOnImage(self):
        blur_gray = cv2.GaussianBlur(self.__m_PageImageToCrop.copy(), (LineCropper.__k_KernelSize, LineCropper.__k_KernelSize), 0)
        edges = cv2.Canny(blur_gray, LineCropper.__k_LowThreshold, LineCropper.__k_HighThreshold)

        return cv2.HoughLinesP(edges, 1, np.pi / 180, LineCropper.__k_CannyThreshold, np.array([]), LineCropper.__k_MinLineLength, LineCropper.__k_MaxLineGap)

    def __getNecessaryLines(self, i_NumpyArr):
        self.__m_YIndexList = []
        self.__m_ProcessedImageToCrop = []

        for line in i_NumpyArr:
            if line[0][1] == line[0][3] and self.__distinctLineCheck(line[0][1]):
                self.__m_ProcessedImageToCrop.append(line)
                self.__m_YIndexList.append(line[0][1])

    def __sortProcessedPageImage(self):
        self.__m_ProcessedImageToCrop = sorted(self.__m_ProcessedImageToCrop, key=lambda x: x[:][0][1])

    def __cropLinesFromPage(self):
        self.__m_LinesList = []
        Utils.CreateFolder(self.__m_PageImageToCropFolderPath)

        for line in self.__m_ProcessedImageToCrop:
            self.__cropNewLine(line[0][1])

    def __distinctLineCheck(self, i_NumToCheck):
        result = True

        if len(self.__m_YIndexList) != 0:
            for lineYIndex in self.__m_YIndexList:
                if abs(i_NumToCheck - lineYIndex) < LineCropper.__k_LineWidth / 2:
                    result = False
                    break

        return result

    def __cropNewLine(self, i_YIndexToCrop):
        if i_YIndexToCrop - LineCropper.__k_LineWidth < 0:
            lineImage = self.__m_PageImageToCrop[0:i_YIndexToCrop + 20, 0:4212]
        else:
            lineImage = self.__m_PageImageToCrop[i_YIndexToCrop - LineCropper.__k_LineWidth + 15:i_YIndexToCrop + 20, 0:4212]

        self.__m_NumberOfLinesInPage += 1
        lineFilePath = self.__m_PageImageToCropFolderPath + "/line{0}.png".format(self.__m_NumberOfLinesInPage)
        lineFolderPath = self.__m_PageImageToCropFolderPath + "/line{0}".format(self.__m_NumberOfLinesInPage)
        cv2.imwrite(lineFilePath, lineImage)
        self.__m_LinesList.append(Line(self.__m_NumberOfLinesInPage, lineFolderPath, lineFilePath))

    def __saveHoughLinesPResultImage(self):
        line_image = np.copy(self.__m_PageImageToCrop.copy()) * 0

        for line in self.__m_ProcessedImageToCrop:
            for x1, y1, x2, y2 in line:
                cv2.line(line_image, (x1, y1), (x2, y2), (255, 0, 0), 5)

        lines_edges = cv2.addWeighted(self.__m_PageImageToCrop.copy(), 0.8, line_image, 1, 0)
        cv2.imwrite(self.__m_PageImageToCropFolderPath + "/lines_edges_test.png", lines_edges)
