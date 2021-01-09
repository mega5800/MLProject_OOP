import cv2
import os

class WordCropper:
    def __init__(self, i_LineImage, i_LineImageFolderPath):
        self.__m_NumberOfWordsInLine = 0
        self.__m_LineImageToCrop = i_LineImage
        self.__m_LineImageToCropFolderPath = i_LineImageFolderPath


    def GetWordsList(self):
        self.__cropWordsFromPage()

        return self.__m_WordsList

    def __cropWordsFromPage(self):
        self.__m_WordsList = []
        wordsFolderPath = self.__m_LineImageToCropFolderPath+"/line{0}"

        if not os.path.isdir(self.__m_LineImageToCropFolderPath):
            os.mkdir(self.__m_LineImageToCropFolderPath)

        fileName = "/word{0}.png".format(self.__m_NumberOfWordsInLine + 1)
        tempFilePath = self.__m_LineImageToCropFolderPath + fileName
        img = cv2.imread(tempFilePath)
        img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        thresh = cv2.threshold(img, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]

        kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (48, 46))
        morph = cv2.morphologyEx(thresh, cv2.MORPH_DILATE, kernel)
        kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (42, 87))
        morph = cv2.morphologyEx(morph, cv2.MORPH_OPEN, kernel)

        cntrs = cv2.findContours(morph, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        cntrs = cntrs[0] if len(cntrs) == 2 else cntrs[1]

        result = img.copy()
        for c in cntrs:
            box = cv2.boundingRect(c)
            x, y, w, h = box
            cv2.rectangle(result, (x, y), (x + w, y + h), (0, 0, 255), 2)

        cv2.imwrite(tempFilePath, result)
