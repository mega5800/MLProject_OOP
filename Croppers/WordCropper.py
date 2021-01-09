from Croppers.Cropper import Cropper

class WordCropper(Cropper):
    def __init__(self, i_LineImage, i_LineImageFolderPath):
        self.__m_NumberOfWordsInLine = 0
        self.__m_LineImageToCrop = i_LineImage
        self.__m_LineImageToCropFolderPath = i_LineImageFolderPath

    def GetItemsList(self):
        Utils.CreateFolder(self.__m_LineImageToCropFolderPath)
        self.__cropWordsFromPage()
        self.__saveContoursImage()

        return self.__m_WordsList

    # יש כפל קוד!!!!
    # לבצע חלוקה נכונה למתודות במקום לשכפל קוד
    def __cropWordsFromPage(self):
        self.__m_WordsList = []

        img = self.__m_LineImageToCrop.copy()
        thresh = cv2.threshold(img, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]

        kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (48, 46))
        morph = cv2.morphologyEx(thresh, cv2.MORPH_DILATE, kernel)
        kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (42, 87))
        morph = cv2.morphologyEx(morph, cv2.MORPH_OPEN, kernel)

        contoursList = cv2.findContours(morph, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        contoursList = contoursList[0] if len(contoursList) == 2 else contoursList[1]
        contoursList = self.__sortContoursList(contoursList)

        for c in contoursList:
            box = cv2.boundingRect(c)
            x, y, w, h = box
            wordToCrop = self.__m_LineImageToCrop[y:y+h, x:x+w]
            self.__m_NumberOfWordsInLine += 1
            wordFilePath = self.__m_LineImageToCropFolderPath + "/word{0}.png".format(self.__m_NumberOfWordsInLine)
            wordFolderPath = self.__m_LineImageToCropFolderPath + "/word{0}".format(self.__m_NumberOfWordsInLine)
            self.__m_WordsList.append(Word(self.__m_NumberOfWordsInLine, wordFolderPath, wordFilePath))
            cv2.imwrite(wordFilePath, wordToCrop)

    def __sortContoursList(self, i_ContoursList):
        return sorted(i_ContoursList, key=lambda ctr: cv2.boundingRect(ctr)[0], reverse=True)

    def __saveContoursImage(self):
        img = self.__m_LineImageToCrop.copy()
        thresh = cv2.threshold(img, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]

        kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (48, 46))
        morph = cv2.morphologyEx(thresh, cv2.MORPH_DILATE, kernel)
        kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (42, 87))
        morph = cv2.morphologyEx(morph, cv2.MORPH_OPEN, kernel)

        contoursList = cv2.findContours(morph, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        contoursList = contoursList[0] if len(contoursList) == 2 else contoursList[1]
        contoursList = self.__sortContoursList(contoursList)

        result = img.copy()
        for c in contoursList:
            box = cv2.boundingRect(c)
            x, y, w, h = box
            cv2.rectangle(result, (x, y), (x + w, y + h), (0, 0, 255), 2)

        cv2.imwrite(self.__m_LineImageToCropFolderPath + "/words_edges_test.png", result)

import cv2
from Classes.Utils import Utils
from Classes.Word import Word
