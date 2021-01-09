from abc import ABC, abstractmethod

class Cropper(ABC):
    @abstractmethod
    def GetItemsList(self):
        pass
