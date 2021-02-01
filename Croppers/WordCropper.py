from Croppers.Cropper import Cropper

class WordCropper(Cropper):
    def __init__(self, i_LineImage, i_LineImageFolderPath):
        super(WordCropper, self).__init__(i_LineImage, i_LineImageFolderPath)

    def GetItemsList(self):
        Utils.CreateFolder(self._m_ItemImageFolderPath)
        self.__cropWordsFromLine()
        self.__saveContoursImage()

        return self.__m_WordsList

    def __cropWordsFromLine(self):
        self.__m_WordsList = []
        thresh = self.__getThreshValue()
        morph = self.__performStructuringElementAndGetMorphValue(thresh)
        self.__getSortedContoursList(morph)

        for c in self.__m_ContoursList:
            box = cv2.boundingRect(c)
            x, y, w, h = box
            wordToCrop = self._m_ItemImage[y:y + h, x:x + w]
            self._m_ItemCounter += 1
            wordFilePath = self._m_ItemImageFolderPath + "/word{0}.png".format(self._m_ItemCounter)
            wordFolderPath = self._m_ItemImageFolderPath + "/word{0}".format(self._m_ItemCounter)
            cv2.imwrite(wordFilePath, wordToCrop)
            self.__m_WordsList.append(Word(self._m_ItemCounter, wordFolderPath, wordFilePath))

    def __getThreshValue(self):
        img = self._m_ItemImage.copy()
        thresh = cv2.threshold(img, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]

        return thresh

    def __performStructuringElementAndGetMorphValue(self, i_ThresholdValue):
        kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (48, 46))
        morph = cv2.morphologyEx(i_ThresholdValue, cv2.MORPH_DILATE, kernel)
        kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (42, 87))
        morph = cv2.morphologyEx(morph, cv2.MORPH_OPEN, kernel)

        return morph

    def __getSortedContoursList(self, i_MorphValue):
        self.__m_ContoursList = cv2.findContours(i_MorphValue, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        self.__m_ContoursList = self.__m_ContoursList[0] if len(self.__m_ContoursList) == 2 else self.__m_ContoursList[1]
        self.__m_ContoursList = self.__sortContoursList(self.__m_ContoursList)

    def __sortContoursList(self, i_ContoursList):
        return sorted(i_ContoursList, key=lambda ctr: cv2.boundingRect(ctr)[0], reverse=True)

    def __saveContoursImage(self):
        result = self._m_ItemImage.copy()
        for c in self.__m_ContoursList:
            box = cv2.boundingRect(c)
            x, y, w, h = box
            cv2.rectangle(result, (x, y), (x + w, y + h), (0, 0, 255), 2)

        cv2.imwrite(self._m_ItemImageFolderPath + "/words_edges_test.png", result)


import cv2
from Classes.Utils import Utils
from Classes.Word import Word
