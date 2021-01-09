import os
import cv2

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
