import threading

class ThreadManager:
    def __init__(self):
        self.__m_ThreadsList = []

    def AddNewThreadToThreadsList(self, i_ThreadToAdd):
        self.__m_ThreadsList.append(i_ThreadToAdd)
        self.__m_ThreadsList[-1].start()

    def PerformJoinFunctionOnThreadsList(self):
        for thread in self.__m_ThreadsList:
            thread.join()
