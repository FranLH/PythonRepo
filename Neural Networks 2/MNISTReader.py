# MNIST image reader
from mnist import MNIST

#TrainImages = 'archive\train-images-idx3-ubyte'
mndata = MNIST("archive",mode="vanilla",gz=False)
# mndata = MNIST("archive")
# 
#images, labels = mndata.load_training()
# # or
images, labels = mndata.load_testing()

print(mndata.display(images[0]))
print(labels[0])

    
#print(mndata.load_testing())