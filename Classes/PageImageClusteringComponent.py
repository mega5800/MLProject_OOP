from keras.preprocessing import image
from keras.applications.vgg16 import VGG16
from keras.applications.vgg16 import preprocess_input
import numpy as np
from sklearn.cluster import KMeans
import shutil
import glob

class PageImageClusteringComponent:
    def __init__(self, i_PageImageFolderPath, i_PageImageResultFolderPath, i_CategoriesNumber):
        self.__m_PageImageFolderPath = i_PageImageFolderPath
        self.__m_PageImageResultFolderPath = i_PageImageResultFolderPath
        self.__m_CategoriesNumber = i_CategoriesNumber
        self.__m_TempLetterList = []
        self.__m_LettersList = []
        self.__m_FeatureList = []

        image.LOAD_TRUNCATED_IMAGES = True
        self.__startImageClusteringOnPageImage()

    def __startImageClusteringOnPageImage(self):
        self.__saveAllLettersImagesInLettersList()
        self.__extractFeaturesFromLettersList()
        self.__preformKMeansAlgorithmAndSaveResults()
        self.__clearAllLists()

    def __saveAllLettersImagesInLettersList(self):
        numberOfLinesFolders = len(glob.glob(self.__m_PageImageFolderPath + "/*/")) + 1

        for linesFolderIndex in range(1, numberOfLinesFolders):
            linesFolderPath = self.__m_PageImageFolderPath + r"\line{0}".format(linesFolderIndex)
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
        kMeansResult = KMeans(n_clusters=self.__m_CategoriesNumber, random_state=0).fit(np.array(self.__m_FeatureList))
        for item, category in enumerate(kMeansResult.labels_):
            shutil.copy(self.__m_LettersList[item], self.__m_PageImageResultFolderPath + r"\category = {0}\i = {1}.png".format(category + 1, item))

    def __clearAllLists(self):
        self.__m_TempLetterList.clear()
        self.__m_LettersList.clear()
        self.__m_FeatureList.clear()
