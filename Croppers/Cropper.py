from abc import ABC, abstractmethod

# לטפל בפונקציית בנאי

class Cropper(ABC):
    @abstractmethod
    def GetItemsList(self):
        pass
