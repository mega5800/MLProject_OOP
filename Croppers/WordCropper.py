from Croppers.Cropper import Cropper

class WordCropper(Cropper):
    def __init__(self, i_LineImage, i_LineImageFolderPath):
        super(WordCropper, self).__init__(i_LineImage, i_LineImageFolderPath)

    def GetItemsList(self):
        Utils.CreateFolder(self._m_ItemImageFolderPath)
        self.__cropWordsFromLine()
        #self.__drawLinesOnImageUsingWordSegmentationList(self._m_ItemImage.copy())

        return self.__m_WordsList

    def __cropWordsFromLine(self):
        self.__m_WordsList = []
        self.__m_NumberMap = []
        self.__m_WordSegmentationList = []
        
        lineImageWithoutLines = Utils.DeleteLinesFromImage(self._m_ItemImage.copy())
        Utils.ConvertImageToNumberMap(self.__m_NumberMap, lineImageWithoutLines, i_UsingTheFunctionForLetterCropper=False)
        self.__drawVerticalLinesOnImage(lineImageWithoutLines)
        blackAndWhite = Utils.ConvertImageToBlackAndWhite(lineImageWithoutLines)
        Utils.ConvertImageToNumberMap(self.__m_NumberMap, blackAndWhite, i_UsingTheFunctionForLetterCropper=False)
        self.__getWordsLinesInGivenImageByNumberList()
        self.__cropWordsFromImageUsingWordSegmentationList(self._m_ItemImage.copy())

    def __drawVerticalLinesOnImage(self, i_ImageToDraw):
        isFirstLineDrawn = False
        avgValueInList = Utils.GetAverageValueFromNumberList(self.__m_NumberMap)

        for i in range(len(self.__m_NumberMap)):
            if self.__m_NumberMap[i] <= avgValueInList and not isFirstLineDrawn:
                isFirstLineDrawn = True
                Utils.DrawLineOnImageAtGivenIndex(i_ImageToDrawOn=i_ImageToDraw, i_ImageShapeIndex=0, i_Index=i, i_Color=0)

            if self.__m_NumberMap[i] >= avgValueInList and isFirstLineDrawn:
                isFirstLineDrawn = False
                Utils.DrawLineOnImageAtGivenIndex(i_ImageToDrawOn=i_ImageToDraw, i_ImageShapeIndex=0, i_Index=i, i_Color=0)

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
            wordImage = i_ImageToCrop[0:i_ImageToCrop.shape[1], wordSeg.FirstLineOfWord: wordSeg.SecondLineOfWord]
            cv2.imwrite(wordFilePath, wordImage)
            self.__m_WordsList.append(Word(self._m_ItemCounter, wordFolderPath, wordFilePath))
            os.remove(wordFilePath)

    def __drawLinesOnImageUsingWordSegmentationList(self, i_ImageToDraw):
        for wordSeg in self.__m_WordSegmentationList:
            Utils.DrawLineOnImageAtGivenIndex(i_ImageToDrawOn=i_ImageToDraw, i_ImageShapeIndex=0, i_Index=wordSeg.FirstLineOfWord, i_Color=0)
            Utils.DrawLineOnImageAtGivenIndex(i_ImageToDrawOn=i_ImageToDraw, i_ImageShapeIndex=0, i_Index=wordSeg.SecondLineOfWord, i_Color=0)

        cv2.imwrite(self._m_ItemImageFolderPath + "/words_lines_marks.png", i_ImageToDraw)

import cv2
import os
import collections
from Classes.Utils import Utils
from Classes.Word import Word
