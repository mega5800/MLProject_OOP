import glob
import threading

from ImageClusteringComponents.PageImageClusteringComponent import PageImageClusteringComponent
from Utilities.ThreadManager import ThreadManager
from Utilities.Utils import Utils

class PDFBookClusteringComponent:
    def __init__(self, i_RootFolderPath, i_CategoriesNumber):
        self.__m_CategoriesNumber = i_CategoriesNumber
        self.__m_RootFolderPath = i_RootFolderPath
        self.__m_SubFoldersInRootFolderPathCounter = len(glob.glob(self.__m_RootFolderPath + "/*/")) + 1
        self.__m_PageImageClusteringComponentList = []
        self.__m_ThreadManager = ThreadManager()
        self.__startImageClusteringOnPDFBook()

    def __startImageClusteringOnPDFBook(self):
        for subFolderIndex in range(1, self.__m_SubFoldersInRootFolderPathCounter):
            self.__m_CurrentPageImageFolder = self.__m_RootFolderPath + r"\page{0}".format(subFolderIndex)
            self.__createResultsFolderAndCategoryFolders(subFolderIndex)
            self.__m_ThreadManager.AddNewThreadToThreadsList(threading.Thread(target=self.__addNewPageImageClusteringComponentToPageImageClusteringComponentList))

        self.__m_ThreadManager.PerformJoinFunctionOnThreadsList()

    def __addNewPageImageClusteringComponentToPageImageClusteringComponentList(self):
        self.__m_PageImageClusteringComponentList.append(PageImageClusteringComponent(self.__m_CurrentPageImageFolder, self.__m_CurrentPageImageResultFolder, self.__m_CategoriesNumber))

    def __createResultsFolderAndCategoryFolders(self, i_PageIndex):
        self.__m_CurrentPageImageResultFolder = self.__m_RootFolderPath + r"\page{0} results".format(i_PageIndex)
        Utils.CreateFolder(self.__m_CurrentPageImageResultFolder)

        for i in range(1, self.__m_CategoriesNumber + 1):
            Utils.CreateFolder(self.__m_CurrentPageImageResultFolder + r"\category = {0}".format(i))
