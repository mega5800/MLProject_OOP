from Croppers.Cropper import Cropper

class WordCropper(Cropper):
    def __init__(self, i_LineImage, i_LineImageFolderPath):
        super(WordCropper, self).__init__(i_LineImage, i_LineImageFolderPath)

    def GetItemsList(self):
        Utils.CreateFolder(self._m_ItemImageFolderPath)
        self.__cropWordsFromLine()
        self.__drawLinesOnImageUsingWordSegmentationList(self._m_ItemImage.copy())

        return self.__m_WordsList

    def __cropWordsFromLine(self):
        self.__m_WordsList = []
        self.__m_NumberMap = []
        self.__m_WordSegmentationList = []

        lineImageWithoutLines = self.__deleteLinesFromImage(self._m_ItemImage.copy())
        self.__convertImageToNumberMap(lineImageWithoutLines)
        self.__drawVerticalLinesOnImage(lineImageWithoutLines)
        blackAndWhite = self.__convertImageToBlackAndWhite(lineImageWithoutLines)
        self.__convertImageToNumberMap(blackAndWhite)
        self.__getWordsLinesInGivenImageByNumberList()
        self.__cropWordsFromImageUsingWordSegmentationList(self._m_ItemImage.copy())

    def __deleteLinesFromImage(self, i_Image):
        getTheUpperLineInfoFlag = False

        thresh = cv2.threshold(i_Image, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]
        horizontal_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (25, 1))
        detected_lines = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, horizontal_kernel, iterations=2)
        cnts = cv2.findContours(detected_lines, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        cnts = cnts[0] if len(cnts) == 2 else cnts[1]
        cnts = sorted(cnts, key=lambda ctr: cv2.boundingRect(ctr)[1])
        for c in cnts:
            if not getTheUpperLineInfoFlag:
                box = cv2.boundingRect(c)
                x, y, w, h = box
                yIndexToCrop = max(y, h) + 5 if max(y, h) + 5 < 120 else 119
                i_Image = self.__cleanImageAboveUpperLine(i_Image, yIndexToCrop)
                getTheUpperLineInfoFlag = True

            cv2.drawContours(i_Image, [c], -1, (255, 255, 255), 2)

        return i_Image

    def __cleanImageAboveUpperLine(self, i_Image, i_MaxYIndex):
        for imageWidthIndex in range(i_MaxYIndex):
            for imageHeightIndex in range(i_Image.shape[1]):
                i_Image[imageWidthIndex, imageHeightIndex] = 255

        return i_Image

    def __convertImageToNumberMap(self, i_ImageToConvert):
        self.__m_NumberMap.clear()

        for imageHeightIndex in range(i_ImageToConvert.shape[1]):
            columnSum = 0

            for imageWidthIndex in range(i_ImageToConvert.shape[0]):
                columnSum += i_ImageToConvert[imageWidthIndex, imageHeightIndex]

            self.__m_NumberMap.append(columnSum // i_ImageToConvert.shape[0])

    def __drawVerticalLinesOnImage(self, i_ImageToDraw):
        isFirstLineDrawn = False
        avgValueInList = self.__getAverageValueFromNumberList()

        for i in range(len(self.__m_NumberMap)):
            if self.__m_NumberMap[i] <= avgValueInList and not isFirstLineDrawn:
                isFirstLineDrawn = True
                self.__drawVerticalLineOnImageAtGivenIndex(i_ImageToDraw, i)

            if self.__m_NumberMap[i] >= avgValueInList and isFirstLineDrawn:
                isFirstLineDrawn = False
                self.__drawVerticalLineOnImageAtGivenIndex(i_ImageToDraw, i)

    def __drawVerticalLineOnImageAtGivenIndex(self, i_ImageToDraw, i_Index):
        for i in range(i_ImageToDraw.shape[0]):
            i_ImageToDraw[i, i_Index] = 0

    def __getAverageValueFromNumberList(self):
        return sum(self.__m_NumberMap) // len(self.__m_NumberMap)

    def __convertImageToBlackAndWhite(self, i_Image):
        imageCopy = i_Image.copy()
        avgImageValue = self.__getAverageValueFromImage(i_Image)
        result = cv2.threshold(imageCopy, avgImageValue, 255, cv2.THRESH_BINARY)[1]

        return result

    def __getAverageValueFromImage(self, i_Image):
        imageCellCounter = 0
        imageCellSum = 0

        for imageWidthIndex in range(i_Image.shape[0]):
            for imageHeightIndex in range(i_Image.shape[1]):
                imageCellCounter += 1
                imageCellSum += i_Image[imageWidthIndex, imageHeightIndex]

        return imageCellSum // imageCellCounter

    def __getWordsLinesInGivenImageByNumberList(self):
        isFirstLineDrawn = False
        avgBetweenBlackLines = self.__getAvgBetweenBlackLines()
        WordSegmentation = collections.namedtuple('WordSegmentation', ['FirstLineOfWord', 'SecondLineOfWord'])

        for i in range(len(self.__m_NumberMap)):
            if self.__m_NumberMap[i] == 0 and not isFirstLineDrawn:
                firstIndex = i
                isFirstLineDrawn = True

            if self.__m_NumberMap[i] == 255 and isFirstLineDrawn and self.__avgDistanceCheck(i, avgBetweenBlackLines):
                secondIndex = i
                self.__m_WordSegmentationList.append(WordSegmentation(firstIndex, secondIndex))
                isFirstLineDrawn = False

        self.__m_WordSegmentationList.reverse()

    def __getAvgBetweenBlackLines(self):
        sum = 0
        counter = 0
        result = 0

        for i in self.__m_NumberMap:
            if i != 0:
                sum += 1
            else:
                counter += 1

        if counter != 0:
            result = sum // counter

        return result

    def __avgDistanceCheck(self, i_Index, i_BlackCellAvg):
        result = True
        loopIndex = i_Index

        while loopIndex < len(self.__m_NumberMap) and loopIndex <= i_BlackCellAvg + i_Index:
            if self.__m_NumberMap[loopIndex] != 255:
                result = False
                break

            loopIndex += 1

        return result

    def __cropWordsFromImageUsingWordSegmentationList(self, i_ImageToCrop):
        for wordSeg in self.__m_WordSegmentationList:
            self._m_ItemCounter += 1
            wordFilePath = self._m_ItemImageFolderPath + "/word{0}.png".format(self._m_ItemCounter)
            wordFolderPath = self._m_ItemImageFolderPath + "/word{0}".format(self._m_ItemCounter)
            self.__m_WordsList.append(Word(self._m_ItemCounter, wordFolderPath, wordFilePath))
            wordImage = i_ImageToCrop[0:i_ImageToCrop.shape[1], wordSeg.FirstLineOfWord: wordSeg.SecondLineOfWord]
            cv2.imwrite(wordFilePath, wordImage)

    def __drawLinesOnImageUsingWordSegmentationList(self, i_ImageToDraw):
        for wordSeg in self.__m_WordSegmentationList:
            self.__drawVerticalLineOnImageAtGivenIndex(i_ImageToDraw, wordSeg.FirstLineOfWord)
            self.__drawVerticalLineOnImageAtGivenIndex(i_ImageToDraw, wordSeg.SecondLineOfWord)

        cv2.imwrite(self._m_ItemImageFolderPath + "/words_lines_marks.png", i_ImageToDraw)

import cv2
import collections
from Classes.Utils import Utils
from Classes.Word import Word
