class CropperFactory:
    @staticmethod
    def CreateCropper(i_CropperFactoryContext, i_ItemImage, i_ItemFolderPath):
        cropperToCreate = None

        if i_CropperFactoryContext == eCropperFactoryContext.CreateLineCropper:
            cropperToCreate = LineCropper(i_ItemImage, i_ItemFolderPath)
        elif i_CropperFactoryContext == eCropperFactoryContext.CreateWordCropper:
            cropperToCreate = WordCropper(i_ItemImage, i_ItemFolderPath)

        return cropperToCreate


from Enums.eCropperFactoryContext import eCropperFactoryContext
from Croppers.LineCropper import LineCropper
from Croppers.WordCropper import WordCropper
