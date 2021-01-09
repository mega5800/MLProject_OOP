from abc import ABC, abstractmethod

# item can be line, word, letter
class Cropper(ABC):
    def __init__(self, i_ItemImage, i_ItemImageFolderPath):
        self._m_ItemCounter = 0
        self._m_ItemImage = i_ItemImage
        self._m_ItemImageFolderPath = i_ItemImageFolderPath

    @abstractmethod
    def GetItemsList(self):
        pass
