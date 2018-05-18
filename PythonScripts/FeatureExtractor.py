'''
Helper class for feature extraction in EmoDash

S. B.

'''


import numpy as np
import pandas as pd

from sklearn.model_selection import cross_val_score
from sklearn.model_selection import KFold
from sklearn.preprocessing import LabelEncoder
from sklearn.pipeline import Pipeline
from pyAudioAnalysis import audioBasicIO
from pyAudioAnalysis import audioFeatureExtraction
import os
import re
import matplotlib.pyplot as plt
from sklearn.externals import joblib
from scipy.stats import kurtosis
from scipy.stats import skew

import array
from pydub import AudioSegment
from pydub.utils import get_array_type
import pandas as pd
# from matplotlib import pyplot as plt
import pickle

class FeatureExtractor:

    def __init__(self, filename_mean_sd, BIT_PRECISION=8):
        # load weights
        #self.dictionary = pickle.load(open(filename_mean_sd, "rb"))
        self.dictionary = pd.read_csv(open(filename_mean_sd, "rb")).to_dict('list')
        self.mean_train = self.dictionary.get("mean")
        self.sd_train = self.dictionary.get("sd")
        self.BIT_PRECISION=BIT_PRECISION

    #Helper method
    #assumption, we save a file somewhere.

    def extract_features(self, file_path):

        [Fs, x] = audioBasicIO.readAudioFile(file_path)
        x= audioBasicIO.stereo2mono(x) #necessary conversion for pyaudio analysis
        features = audioFeatureExtraction.stFeatureExtraction(x, Fs, 0.05*Fs, 0.025*Fs)
        features = np.mean(features, axis=1)
        features = np.asarray(features).reshape(len(features),-1).transpose()
        #features_complete = np.append(features_complete, features, axis=0)
        return features #_complete

    def extract_features2(self, Fs, x):
        x = audioBasicIO.stereo2mono(x)  # necessary conversion for pyaudio analysis
        #print len(x)

        # they must be 24k samples
        #coef = int(np.floor(len(x)/48000))

        #x = x[range(0,len(x),6)]
        #print len(x)
        # Fs=16000

        features = audioFeatureExtraction.stFeatureExtraction(x, Fs, 0.05 * Fs, 0.025 * Fs)
        if len(features) == 0:
            features = np.zeros((34, 2))

        features_mean = np.mean(features, axis=1)
        features_std = np.std(features, axis=1)
        features_kurtosis = kurtosis(features, axis=1)
        features_skew = skew(features, axis=1)

        vec4moments = np.append(np.append(np.append(features_mean, features_std), features_kurtosis), features_skew)

        result = np.asarray(vec4moments).reshape(len(vec4moments), -1).transpose()
        #print(np.shape(result))
        # features_complete = np.append(features_complete, features, axis=0)
        return result#vec4moments  # _complete


    def extract_features3(self, Fs, x):
        x = audioBasicIO.stereo2mono(x)  # necessary conversion for pyaudio analysis

        # they must be 24k samples
        #coef = int(np.floor(len(x)/48000))

        #x = x[range(0,len(x),6)]
        #print len(x)
        # Fs=16000

        features = audioFeatureExtraction.stFeatureExtraction(x, Fs, 0.05 * Fs, 0.025 * Fs)
        if len(features) == 0:
            features = np.zeros((34, 119))

        #features = np.mean(features, axis=1)
        features = np.asarray(features).reshape(len(features), -1).transpose()
        print len(features)
        # features_complete = np.append(features_complete, features, axis=0)
        return features  # _complete


    def split_song2(self,song,padding_length):
        bit_depth = song.sample_width * self.BIT_PRECISION
        array_type = get_array_type(bit_depth)
        numeric_array = array.array(array_type, song._data)
        numeric_array = numeric_array.tolist()
        features = self.extract_features3(song.frame_rate, np.asarray(numeric_array))
        #print("$$")
        #print(len(features))

        while len(features)<padding_length:
            features=np.append(features,(np.zeros((1,34)))) #padding

        if len(features)>padding_length:
            features= features[len(features)-padding_length:len(features)]
        #print(np.shape(features))

        print(len(features))
        #print("$$")
        return features

    def split_song(self, song):
        mydict = []
        convers = []

        for i in range(3000, len(song)+3000, 3000):
            # print i
            splitting = song[i - 3000:i]  # first three seconds
            bit_depth = splitting.sample_width * self.BIT_PRECISION
            # print splitting.frame_rate
            array_type = get_array_type(bit_depth)
            numeric_array = array.array(array_type, splitting._data)
            numeric_array = numeric_array.tolist()
            features = self.extract_features2(splitting.frame_rate, np.asarray(numeric_array))[0]
            features_transformed = (features - self.mean_train) / self.sd_train
            convers.append(features_transformed)
            #if len(convers) == 3:
            #    prediction = self.my_attention_network.predict(np.array([convers]))[0]
                # print prediction
            #    mydict.append({"Anger": prediction[0], "Disgust": prediction[1], "Fear": prediction[3],
            #                   "Happiness": prediction[5], "Neutral": prediction[6], "Sadness": prediction[2],
            #                   "Surprise": prediction[4]})
            #    convers.pop(0)

        return convers
