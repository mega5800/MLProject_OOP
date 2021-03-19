import os
import cv2
import numpy as np

class Utils:
    @staticmethod
    def CreateFolder(i_FolderPath):
        if not os.path.isdir(i_FolderPath):
            os.mkdir(i_FolderPath)

    @staticmethod
    def ConvertPNGFileToGrayScale(i_ImageFilePath):
        imgToConvert = cv2.imread(i_ImageFilePath)
        imgToConvert = cv2.cvtColor(imgToConvert, cv2.COLOR_BGR2GRAY)

        return imgToConvert

    @staticmethod
    def ConvertImageToNumberMap(i_NumberMap, i_ImageToConvert, i_UsingTheFunctionForLetterCropper):
        i_NumberMap.clear()
        imageShapeIndex = 0 if i_UsingTheFunctionForLetterCropper else 1

        for i in range(i_ImageToConvert.shape[imageShapeIndex]):
            if i_UsingTheFunctionForLetterCropper:
                columnSum = np.sum(i_ImageToConvert[i, :])
                i_NumberMap.append(columnSum // i_ImageToConvert.shape[1])
            else:
                columnSum = np.sum(i_ImageToConvert[:, i])
                i_NumberMap.append(columnSum // i_ImageToConvert.shape[0])

    @staticmethod
    def __cleanImageAboveUpperLine(i_Image, i_MaxYIndex):
        for imageWidthIndex in range(i_MaxYIndex):
            for imageHeightIndex in range(i_Image.shape[1]):
                i_Image[imageWidthIndex, imageHeightIndex] = 255

        return i_Image

    @staticmethod
    def DeleteLinesFromImage(i_Image):
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
                i_Image = Utils.__cleanImageAboveUpperLine(i_Image, yIndexToCrop)
                getTheUpperLineInfoFlag = True

            cv2.drawContours(i_Image, [c], -1, (255, 255, 255), 2)

        return i_Image

    @staticmethod
    def GetAverageValueFromNumberList(i_NumberMap):
        return int(np.mean(i_NumberMap))

    @staticmethod
    def DrawLineOnImageAtGivenIndex(i_ImageToDrawOn, i_ImageShapeIndex, i_Index, i_Color):
        for i in range(i_ImageToDrawOn.shape[i_ImageShapeIndex]):
            if i_Color == 0:
                i_ImageToDrawOn[i, i_Index] = i_Color
            elif i_Color == 255:
                i_ImageToDrawOn[i_Index, i] = i_Color

    @staticmethod
    def ConvertImageToBlackAndWhite(i_Image):
        avgImageValue = Utils.GetAverageValueFromImage(i_Image)
        return np.where(i_Image > avgImageValue, 255, 0)

    @staticmethod
    def GetAverageValueFromImage(i_Image):
        return int(np.mean(i_Image))