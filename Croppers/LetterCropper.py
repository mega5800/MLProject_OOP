from Croppers.Cropper import Cropper

class LetterCropper(Cropper):
    def __init__(self, i_WordImage, i_WordImageFolderPath):
        super(LetterCropper, self).__init__(i_WordImage, i_WordImageFolderPath)

    def GetItemsList(self):
        Utils.CreateFolder(self._m_ItemImageFolderPath)
        self.cropLettersFromWord()
        self.__m_cppLetterCropper.SaveLetterMarkingFile()

    def cropLettersFromWord(self):
        imageFolderPath = os.path.normpath(self._m_ItemImageFolderPath)
        imageFilePath = os.path.normpath(self._m_ItemImage)

        self.__m_cppLetterCropper = CVCodeInCPP.CPPLetterCropper()
        self.__m_cppLetterCropper.SavingFilePath = imageFolderPath
        self.__m_cppLetterCropper.ImageFilePath = imageFilePath
        self.__m_cppLetterCropper.CropLettersFromImage()

import CVCodeInCPP
import os
from Classes.Utils import Utils
