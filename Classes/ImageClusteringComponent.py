from keras.preprocessing import image
from keras.applications.vgg16 import VGG16
from keras.applications.vgg16 import preprocess_input
import numpy as np
from sklearn.cluster import KMeans
import shutil, glob

from Classes.Utils import Utils

class ImageClusteringComponent:
    __k_CategoriesNumber = 40

    def __init__(self, i_RootFolderPath):
        self.__m_RootFolderPath = i_RootFolderPath
        self.__m_SubFoldersInRootFolderPathCounter = len(glob.glob(self.__m_RootFolderPath + "/*/")) + 1
        self.__m_TempLetterList = []
        self.__m_LettersList = []
        self.__m_FeatureList = []

        image.LOAD_TRUNCATED_IMAGES = True

    def StartImageClustering(self):
        for subFolderIndex in range(1, self.__m_SubFoldersInRootFolderPathCounter):
            self.__m_CurrentImagesFolder = self.__m_RootFolderPath + r"\page{0}".format(subFolderIndex)
            self.__m_CurrentImagesResultFolder = self.__m_RootFolderPath + r"\page{0} results".format(subFolderIndex)
            Utils.CreateFolder(self.__m_CurrentImagesResultFolder)
            self.__createCategoryFolders()
            self.__saveAllLettersImagesInLettersList()
            self.__extractFeaturesFromLettersList()
            self.__preformKMeansAlgorithmAndSaveResults()
            self.__clearAllLists()

    def __createCategoryFolders(self):
        for i in range(1, ImageClusteringComponent.__k_CategoriesNumber + 1):
            Utils.CreateFolder(self.__m_CurrentImagesResultFolder + r"\category = {0}".format(i))

    def __saveAllLettersImagesInLettersList(self):
        numberOfLinesFolders = len(glob.glob(self.__m_CurrentImagesFolder + "/*/")) + 1

        for linesFolderIndex in range(1, numberOfLinesFolders):
            linesFolderPath = self.__m_CurrentImagesFolder + r"\line{0}".format(linesFolderIndex)
            numberOfWordsFolders = len(glob.glob(linesFolderPath + "/*/")) + 1
            for wordsFolderIndex in range(1, numberOfWordsFolders):
                wordsFolderPath = linesFolderPath + r"\word{0}".format(wordsFolderIndex)
                self.__m_TempLetterList.clear()
                self.__m_TempLetterList = glob.glob1(wordsFolderPath, "*.png")
                for letterPath in self.__m_TempLetterList:
                    self.__m_LettersList.append(wordsFolderPath + r"\{0}".format(letterPath))

    def __extractFeaturesFromLettersList(self):
        model = VGG16(weights='imagenet', include_top=False)

        self.__m_LettersList.sort()
        for i, imagePath in enumerate(self.__m_LettersList):
            img = image.load_img(imagePath, target_size=(224, 224))
            img_data = image.img_to_array(img)
            img_data = np.expand_dims(img_data, axis=0)
            img_data = preprocess_input(img_data)
            features = np.array(model.predict(img_data))
            self.__m_FeatureList.append(features.flatten())

    def __preformKMeansAlgorithmAndSaveResults(self):
        kMeansResult = KMeans(n_clusters=ImageClusteringComponent.__k_CategoriesNumber, random_state=0).fit(np.array(self.__m_FeatureList))
        for item, category in enumerate(kMeansResult.labels_):
            shutil.copy(self.__m_LettersList[item], self.__m_CurrentImagesResultFolder + r"\category = {0}\i = {1}.png".format(category + 1, item))

    def __clearAllLists(self):
        self.__m_TempLetterList.clear()
        self.__m_LettersList.clear()
        self.__m_FeatureList.clear()
