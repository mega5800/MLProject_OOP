import cv2

class Page:
    def __init__(self, i_PageNum, i_PageFilePath):
        self.__m_PageNum = i_PageNum
        self.__m_PageFilePath = i_PageFilePath
        self.__convertAndCropPNGFileToGrayScale()
        # self.__cropPageIntoLines()

    def __convertAndCropPNGFileToGrayScale(self):
        imgToCropAndConvert = cv2.imread(self.__m_PageFilePath)
        imgToCropAndConvert = cv2.cvtColor(imgToCropAndConvert, cv2.COLOR_BGR2GRAY)
        imgToCropAndConvert = imgToCropAndConvert[835:3870, 0:2979]
        self.__m_PageImage = imgToCropAndConvert
        cv2.imwrite(self.__m_PageFilePath, imgToCropAndConvert)

    def __cropPageIntoLines(self):
        self.__m_LinesList = []
