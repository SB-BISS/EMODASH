#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jul 20 11:13:30 2017

@author: guysimons
"""


#############Model architecture##############

from keras import layers
from keras import models
from keras.preprocessing.image import ImageDataGenerator
import os
train_dir = "/Users/guysimons/Documents/BISS/EmoDash/CNN_Development/Databases/SAVEE_EMODB_SPEC/train"
test_dir = "/Users/guysimons/Documents/BISS/EmoDash/CNN_Development/Databases/SAVEE_EMODB_SPEC/test"

total_files_train = 0

for directory in os.listdir(train_dir):
     if directory == ".DS_Store":
          continue
     total = len(os.listdir(os.path.join(train_dir, directory)))
     total_files_train += total

print("total images for training: ", total_files_train)

total_files_test = 0

for directory in os.listdir(test_dir):
     if directory == ".DS_Store":
          continue
     total = len(os.listdir(os.path.join(test_dir, directory)))
     total_files_test += total

print("total images for testing: ", total_files_test)


train_datagen = ImageDataGenerator(rescale=1./255)
test_datagen = ImageDataGenerator(rescale = 1./255)

train_generator = train_datagen.flow_from_directory(train_dir, batch_size=10, target_size=(224,224),class_mode="categorical")
test_generator = train_datagen.flow_from_directory(test_dir, batch_size=10, target_size=(224,224),class_mode="categorical")

model = models.Sequential()
model.add(layers.Conv2D(120, (11,11), strides = 4, activation = 'relu', input_shape=(224,224,3)))
model.add(layers.MaxPooling2D((3,3), strides=2))
model.add(layers.Conv2D(256, (5,5), strides = 1, activation = 'relu'))
model.add(layers.MaxPooling2D((3,3), strides=2))
model.add(layers.Conv2D(384, (3,3), strides = 1, activation = 'relu'))
model.add(layers.Flatten())
model.add(layers.Dense(2048))
model.add(layers.Dropout(0.5))
model.add(layers.Dense(2048))
model.add(layers.Dropout(0.5))
model.add(layers.Dense(7))
model.compile(loss="categorical_crossentropy", optimizer="adam", metrics=["acc"])

history = model.fit_generator(train_generator, steps_per_epoch=74, epochs=20, validation_data=test_generator, validation_steps=20)


