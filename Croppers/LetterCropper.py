import cv2
import numpy as np
from Croppers.Cropper import Cropper

class LetterCropper(Cropper):
    def __init__(self, i_WordImage, i_WordImageFolderPath):
        super(LetterCropper, self).__init__(i_WordImage, i_WordImageFolderPath)

    def GetItemsList(self):
        Utils.CreateFolder(self._m_ItemImageFolderPath)
        self.__saveLettersFromWord()
        self.__saveConnectedComponentsResultImage()

    def __saveLettersFromWord(self):
        self._m_ItemImage = cv2.cvtColor(self._m_ItemImage, cv2.COLOR_BGR2GRAY)
        self.__m_ImageWithoutLines = Utils.DeleteLinesFromImage(self._m_ItemImage.copy())
        self.__m_NumberMap = []

        Utils.ConvertImageToNumberMap(self.__m_NumberMap, self.__m_ImageWithoutLines, i_UsingTheFunctionForLetterCropper=True)
        self.__cleanNoisesInImageWithoutLines()

        avgValue = Utils.GetAverageValueFromImage(self.__m_ImageWithoutLines)
        ret, self.__m_BlackAndWhiteWithoutLinesImage = cv2.threshold(self.__m_ImageWithoutLines.copy(), avgValue, 255, 0)
        self.__m_InvertedBlackAndWhiteWithoutLinesImage = cv2.bitwise_not(self.__m_BlackAndWhiteWithoutLinesImage)
        _, self.__m_ConnectedComponentsMarkers = cv2.connectedComponents(self.__m_InvertedBlackAndWhiteWithoutLinesImage)
        self.__cropLettersFromConnectedComponentsAndSaveThem()

    def __cleanNoisesInImageWithoutLines(self):
        for i in range(len(self.__m_NumberMap)):
            if self.__m_NumberMap[i] >= 250:
                Utils.DrawLineOnImageAtGivenIndex(i_ImageToDrawOn=self.__m_ImageWithoutLines, i_ImageShapeIndex=1, i_Index=i, i_Color=255)

    def __saveConnectedComponentsResultImage(self):
        label_hue = np.uint8(179 * self.__m_ConnectedComponentsMarkers / np.max(self.__m_ConnectedComponentsMarkers))
        blank_ch = 255 * np.ones_like(label_hue)
        labeled_img = cv2.merge([label_hue, blank_ch, blank_ch])
        labeled_img = cv2.cvtColor(labeled_img, cv2.COLOR_HSV2BGR)
        labeled_img[label_hue == 0] = 0

        cv2.imwrite(self._m_ItemImageFolderPath+"/connectedComponentsResult.png", labeled_img)

    def __cropLettersFromConnectedComponentsAndSaveThem(self):
        letterList = []
        contours = cv2.findContours(self.__m_InvertedBlackAndWhiteWithoutLinesImage, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[0]
        contours = sorted(contours, key=lambda ctr: cv2.boundingRect(ctr)[0], reverse=True)

        sum = 0
        countContours = 0
        for cnt in contours:
            (x, y, w, h) = cv2.boundingRect(cnt)
            if h > 10 and w > 10:
                sum += w
                countContours += 1

        if countContours == 0:
            return

        sum //= countContours
        for cnt in contours:
            (x, y, w, h) = cv2.boundingRect(cnt)
            if h > 10 and w > 10:
                letterList.clear()
                amountOfRuns = 1 if w // sum == 0 else w // sum
                for i in range(amountOfRuns):
                    letterList.append(self.__m_ImageWithoutLines[y:y + h, x + ((w * i) // amountOfRuns):x + ((w * (i + 1)) // amountOfRuns)])

                letterList.reverse()
                for image in letterList:
                    self._m_ItemCounter += 1
                    cv2.imwrite(self._m_ItemImageFolderPath + "/letter{}.png".format(self._m_ItemCounter), image)

from Classes.Utils import Utils
