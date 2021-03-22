import winsound
from Classes.ImageClusteringComponent import ImageClusteringComponent


def finishSound():
    frequency = 2500
    duration = 500
    winsound.Beep(frequency, duration)

#book = PDFBooksFolder(r"F:\Python Projects\MLProject_OOP\pdf books")


pythonImageClusteringComponent = ImageClusteringComponent(r"C:\Users\mega5\Desktop\python book1\book1")
cppImageClusteringComponent = ImageClusteringComponent(r"C:\Users\mega5\Desktop\cpp book1\book1")

pythonImageClusteringComponent.StartImageClustering()
finishSound()

cppImageClusteringComponent.StartImageClustering()
finishSound()
