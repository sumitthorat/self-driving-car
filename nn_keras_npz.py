import os,cv2
import time
import glob
import numpy as np


from sklearn.utils import shuffle
from sklearn.model_selection import train_test_split

# from keras import backend as K

# K.set_image_dim_ordering('th')

from keras.utils import np_utils
import keras


from keras.models import Sequential
from keras.layers.convolutional import Conv2D
from keras.layers.convolutional import MaxPooling2D
from keras.layers.core import Activation
from keras.layers.core import Flatten
from keras.layers.core import Dense
from keras.layers.core import Dropout
from keras.optimizers import SGD
from keras import backend as K
K.set_image_dim_ordering('tf')
from keras.optimizers import Adam
from keras.preprocessing.image import ImageDataGenerator

image_array = np.zeros((1, 38400))
label_array = np.zeros((1, 4), 'float')
training_data = glob.glob('IOT_Project/training_data/*.npz')        # Finds filename matching specified path or pattern.

for single_npz in training_data:                        # single_npz == one array representing one array of saved image data and user input label for that image.
    with np.load(single_npz) as data:
        print data.files
        train_temp = data['train']                      # returns the training data image array assigned to 'train' argument created during np.savez step in 'collect_training_data.py'
        train_labels_temp = data['train_labels']        # returns the training user input data array assigned to 'train_labels' argument created during np.savez step in 'collect_training_data.py'
        print train_temp.shape
        print train_labels_temp.shape
    image_array = np.vstack((image_array, train_temp))
    label_array = np.vstack((label_array, train_labels_temp))

X = image_array[1:, :]
y = label_array[1:, :]
print 'Shape of feature array: ', X.shape
print 'Shape of label array: ', y.shape

# # Normalize with l2 (not gonna use this...)
# X = preprocessing.normalize(X, norm='l2')

# Normalize from 0 to 1
X = X / 255.

# train-test split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.15)

model = Sequential()

model.add(Dense(units=32,activation="relu",input_shape=(38400,)))
model.add(Dense(units=32,activation="relu"))
model.add(Dense(units=4,activation="softmax"))
model.compile(optimizer=SGD(0.0001),loss="categorical_crossentropy",metrics=["accuracy"])

hist = model.fit(X_train, y_train, batch_size=16, epochs=20, verbose=1, validation_data=(X_test, y_test))
#H = model.fit_generator(aug.flow(X_train, y_train, batch_size=BS), validation_data=(X_test, y_test), steps_per_epoch=len(X_train) // BS,epochs=EPOCHS, verbose=1)

score = model.evaluate(X_test, y_test, verbose=0)
print('Test Loss:', score[0])
print('Test accuracy:', score[1])
