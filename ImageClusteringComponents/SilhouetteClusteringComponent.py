class SilhouetteClusteringComponent:
    k_MinKValue = 50
    k_MaxKValue = 105

    def __init__(self, i_RootFolderPath, i_FolderIndex):
        self.__m_ImageFilesPathsList = []
        self.__m_SilhouetteValuesList = []
        self.__m_KValuesList = []
        self.__m_RootFolderPath = i_RootFolderPath
        self.__m_FolderIndex = i_FolderIndex
        self.__getSilhouetteValueAndStartKMeansAlgorithm()

    def __getSilhouetteValueAndStartKMeansAlgorithm(self):
        self.__calculateSilhouetteValue()
        self.__createResultsFolderAndCategoryFolders()
        pageImageClusteringComponent = PageImageClusteringComponent(self.__m_RootFolderPath, self.__m_CurrentPageImageResultFolder, self.__m_CategoriesNumber)
        pageImageClusteringComponent.StartImageClusteringOnPageImage()

    def __createResultsFolderAndCategoryFolders(self):
        self.__m_CurrentPageImageResultFolder = self.__m_RootFolderPath + r"\page{0} results".format(self.__m_FolderIndex)
        Utils.CreateFolder(self.__m_CurrentPageImageResultFolder)

        for i in range(1, self.__m_CategoriesNumber + 1):
            Utils.CreateFolder(self.__m_CurrentPageImageResultFolder + r"\category = {0}".format(i))

    def __calculateSilhouetteValue(self):
        pageFolderPath = self.__m_RootFolderPath
        amountOfLinesFolders = len(glob.glob(pageFolderPath + "/*/")) + 1

        for lineFolderIndex in range(1, amountOfLinesFolders):
            lineFolderPath = pageFolderPath + r"\line{0}".format(lineFolderIndex)
            amountOfWordsFolders = len(glob.glob(lineFolderPath + "/*/")) + 1

            for wordFolderIndex in range(1, amountOfWordsFolders):
                wordFolderPath = lineFolderPath + r"\word{0}".format(wordFolderIndex)

                tempList = glob.glob1(wordFolderPath, "*.png")
                for temp in tempList:
                    self.__m_ImageFilesPathsList.append(wordFolderPath + r"\{0}".format(temp))

        images = [cv2.resize(cv2.imread(letterPath), (224, 224)) for letterPath in self.__m_ImageFilesPathsList]
        images = np.array(np.float32(images).reshape(len(images), -1) / 255)

        model = tf.keras.applications.MobileNetV2(include_top=False, weights='imagenet', input_shape=(224, 224, 3))
        predictions = model.predict(images.reshape(-1, 224, 224, 3))
        pred_images = predictions.reshape(images.shape[0], -1)

        for k in range(SilhouetteClusteringComponent.k_MinKValue, SilhouetteClusteringComponent.k_MaxKValue, 5):
            kmeans2 = KMeans(n_clusters=k, random_state=None).fit(pred_images)
            labels = kmeans2.labels_
            self.__m_SilhouetteValuesList.append(silhouette_score(pred_images, labels, metric='euclidean'))
            self.__m_KValuesList.append(k)

        self.__m_CategoriesNumber = self.__getBestKValue()

    def __getBestKValue(self):
        maxSilhouetteValueIndex = self.__m_SilhouetteValuesList.index(max(self.__m_SilhouetteValuesList))
        bestKValue = self.__m_KValuesList[maxSilhouetteValueIndex]

        return bestKValue


import numpy as np
import tensorflow as tf
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score
from Utilities.Utils import Utils
import cv2
import glob
from ImageClusteringComponents.PageImageClusteringComponent import PageImageClusteringComponent
