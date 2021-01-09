import os

class Utils:
    @staticmethod
    def CreateFolder(i_FolderPath):
        if not os.path.isdir(i_FolderPath):
            os.mkdir(i_FolderPath)
