from Croppers.Cropper import Cropper

class LetterCropper(Cropper):
    def __init__(self, i_WordImage, i_WordImageFolderPath):
        super(LetterCropper, self).__init__(i_WordImage, i_WordImageFolderPath)

    def GetItemsList(self):
        a = 5  # need to implement
