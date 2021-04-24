import numpy as np
import tensorflow as tf
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score
import cv2
import glob

class SilhouetteValueCalculator:
    k_MinKValue = 50
    k_MaxKValue = 105

    def __init__(self):
        self.__m_ImageFilesPathsList = []
        self.__m_SilhouetteValuesList = []
        self.__m_KValuesList = []

    def CalculateSilhouetteValue(self, i_RootFolderPath):
        self.__clearAllLists()
        pageFolderPath = i_RootFolderPath
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

        for k in range(SilhouetteValueCalculator.k_MinKValue, SilhouetteValueCalculator.k_MaxKValue, 5):
            print(k)
            kmeans2 = KMeans(n_clusters=k).fit(pred_images)
            labels = kmeans2.labels_
            self.__m_SilhouetteValuesList.append(silhouette_score(pred_images, labels, metric='euclidean'))
            self.__m_KValuesList.append(k)

        return self.__getBestKValue()

    def __getBestKValue(self):
        maxSilhouetteValueIndex = self.__m_SilhouetteValuesList.index(max(self.__m_SilhouetteValuesList))
        bestKValue =  self.__m_KValuesList[maxSilhouetteValueIndex]
        print(bestKValue)

        return bestKValue

    def __clearAllLists(self):
        self.__m_ImageFilesPathsList.clear()
        self.__m_SilhouetteValuesList.clear()
        self.__m_KValuesList.clear()
