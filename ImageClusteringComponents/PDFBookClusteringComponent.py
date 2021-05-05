class PDFBookClusteringComponent:
    k_NumberOfConcurrentFilesToProcess = 3

    def __init__(self, i_RootFolderPath):
        self.__m_RootFolderPath = i_RootFolderPath
        self.__m_SubFoldersInRootFolderPathCounter = len(glob.glob(self.__m_RootFolderPath + "/*/")) + 1
        self.__m_SilhouetteClusteringComponentList = []
        self.__m_ThreadManager = ThreadManager()

        self.__preformSilhouetteCalculation()

    def __preformSilhouetteCalculation(self):
        count = 0
        numModulo = self.__m_SubFoldersInRootFolderPathCounter % PDFBookClusteringComponent.k_NumberOfConcurrentFilesToProcess
        numDivide = self.__m_SubFoldersInRootFolderPathCounter // PDFBookClusteringComponent.k_NumberOfConcurrentFilesToProcess

        for i in range(1, numDivide + 1):
            for n in range(PDFBookClusteringComponent.k_NumberOfConcurrentFilesToProcess):
                count += 1
                self.__m_CurrentPageImageFolder = self.__m_RootFolderPath + r"\page{0}".format(count)
                self.__m_ThreadManager.AddNewThreadToThreadsList(threading.Thread(target=self.__addNewSilhouetteClusteringComponentToSilhouetteClusteringComponentList,args=(self.__m_CurrentPageImageFolder, count,)))

            self.__m_ThreadManager.PerformJoinFunctionOnThreadsList()
            self.__m_ThreadManager.ClearThreadsList()

        for i in range(numModulo):
            count += 1
            self.__m_CurrentPageImageFolder = self.__m_RootFolderPath + r"\page{0}".format(count)
            self.__m_ThreadManager.AddNewThreadToThreadsList(threading.Thread(target=self.__addNewSilhouetteClusteringComponentToSilhouetteClusteringComponentList, args=(self.__m_CurrentPageImageFolder, count,)))

        self.__m_ThreadManager.PerformJoinFunctionOnThreadsList()

    def __addNewSilhouetteClusteringComponentToSilhouetteClusteringComponentList(self, i_PageImageFolder, i_FolderIndex):
        self.__m_SilhouetteClusteringComponentList.append(SilhouetteClusteringComponent(i_PageImageFolder, i_FolderIndex))


from Utilities.ThreadManager import ThreadManager
from ImageClusteringComponents.SilhouetteClusteringComponent import SilhouetteClusteringComponent
import glob
import threading
