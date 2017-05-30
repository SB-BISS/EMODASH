'''
Helper class for feature extraction in EmoDash

S. B.

'''


import numpy as np
import pandas as pd
from keras.models import Sequential
from keras.layers import Dense
from keras.wrappers.scikit_learn import KerasClassifier
from keras.utils import np_utils
from keras.layers import Dropout
from sklearn.model_selection import cross_val_score
from sklearn.model_selection import KFold
from sklearn.preprocessing import LabelEncoder
from keras.optimizers import SGD
from sklearn.pipeline import Pipeline
from pyAudioAnalysis import audioBasicIO
from pyAudioAnalysis import audioFeatureExtraction
import os
import re
import matplotlib.pyplot as plt
from sklearn.externals import joblib

#Helper method
#assumption, we save a file somewhere.

def extract_features(file_path):

    [Fs, x] = audioBasicIO.readAudioFile(file_path)
    x= audioBasicIO.stereo2mono(x) #necessary conversion for pyaudio analysis
    features = audioFeatureExtraction.stFeatureExtraction(x, Fs, 0.05*Fs, 0.025*Fs)
    features = np.mean(features, axis=1)
    features = np.asarray(features).reshape(len(features),-1).transpose()
    #features_complete = np.append(features_complete, features, axis=0)
    return features #_complete




def baseline_model(optimizer = 'adam',units=70, prop=0.3):
    # create model
    model = Sequential()
    model.add(Dense(input_dim=34, output_dim = units, activation='relu'))
    model.add(Dropout(prop))
    model.add(Dense(input_dim = units, output_dim = 7, activation='softmax'))
    
    model.compile(loss='categorical_crossentropy', optimizer=optimizer, metrics=['accuracy'])
    return model

