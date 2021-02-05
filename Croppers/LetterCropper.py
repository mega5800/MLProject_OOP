from Croppers.Cropper import Cropper

class LetterCropper(Cropper):
    def __init__(self, i_WordImage, i_WordImageFolderPath):
        super(LetterCropper, self).__init__(i_WordImage, i_WordImageFolderPath)

    def GetItemsList(self):
        Utils.CreateFolder(self._m_ItemImageFolderPath)
        self.__cropLettersFromWord()
        self.__saveContoursImage()

        return self.__m_LettersList

    def __cropLettersFromWord(self):
        self.__m_LettersList = []

        gray = cv2.cvtColor(self._m_ItemImage.copy(), cv2.COLOR_BGR2GRAY)
        blur = cv2.GaussianBlur(gray, (5, 5), 0)
        canny = cv2.Canny(blur, 120, 255, 1)

        cnts = cv2.findContours(canny, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        self.__m_ContoursList = cnts[0] if len(cnts) == 2 else cnts[1]
        self.__pickSuitableContoursFromContoursList()
        self.__m_ContoursList = sorted(self.__m_ContoursList, key=lambda ctr: cv2.boundingRect(ctr)[0], reverse=True)

        for c in self.__m_ContoursList:
            area = cv2.contourArea(c)
            x, y, w, h = cv2.boundingRect(c)
            letterToCrop = self._m_ItemImage[y:y + h, x:x + w]
            self._m_ItemCounter += 1
            letterFilePath = self._m_ItemImageFolderPath + "/letter{0}.png".format(self._m_ItemCounter)
            letterFolderPath = self._m_ItemImageFolderPath + "/letter{0}".format(self._m_ItemCounter)
            cv2.imwrite(letterFilePath, letterToCrop)
            self.__m_LettersList.append(Letter(self._m_ItemCounter, letterFolderPath, letterFilePath))

    def __pickSuitableContoursFromContoursList(self):
        resultList = []
        savedContoursList = []

        for c in self.__m_ContoursList:
            area = cv2.contourArea(c)
            x, y, w, h = cv2.boundingRect(c)
            if 100 >= w >= 20 and 100 >= h >= 20:
                resultList.append(c)

        self.__m_ContoursList.clear()
        self.__m_ContoursList = resultList

    def __saveContoursImage(self):
        result = self._m_ItemImage.copy()
        for c in self.__m_ContoursList:
            box = cv2.boundingRect(c)
            x, y, w, h = box
            cv2.rectangle(result, (x, y), (x + w, y + h), (0, 0, 255), 2)

        cv2.imwrite(self._m_ItemImageFolderPath + "/letters_edges_test.png", result)

import cv2
from Classes.Utils import Utils
from Classes.Letter import Letter
