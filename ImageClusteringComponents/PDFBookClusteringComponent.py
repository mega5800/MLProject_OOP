class PDFBookClusteringComponent:
    def __init__(self, i_RootFolderPath):
        self.__m_RootFolderPath = i_RootFolderPath
        self.__m_SubFoldersInRootFolderPathCounter = len(glob.glob(self.__m_RootFolderPath + "/*/")) + 1
        self.__m_SilhouetteClusteringComponentList = []
        self.__m_ThreadManager = ThreadManager()

        self.__preformSilhouetteCalculation()

    def __preformSilhouetteCalculation(self):
        for subFolderIndex in range(1, self.__m_SubFoldersInRootFolderPathCounter):
            self.__m_CurrentPageImageFolder = self.__m_RootFolderPath + r"\page{0}".format(subFolderIndex)
            self.__m_ThreadManager.AddNewThreadToThreadsList(threading.Thread(target=self.__addNewSilhouetteClusteringComponentToSilhouetteClusteringComponentList, args=(self.__m_CurrentPageImageFolder,subFolderIndex,)))

        self.__m_ThreadManager.PerformJoinFunctionOnThreadsList()

    def __addNewSilhouetteClusteringComponentToSilhouetteClusteringComponentList(self, i_PageImageFolder, i_FolderIndex):
        self.__m_SilhouetteClusteringComponentList.append(SilhouetteClusteringComponent(i_PageImageFolder, i_FolderIndex))


from Utilities.ThreadManager import ThreadManager
from ImageClusteringComponents.SilhouetteClusteringComponent import SilhouetteClusteringComponent
import glob
import threading
