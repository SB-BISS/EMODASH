#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Thu May  4 13:07:05 2017

@author: guysimons
"""

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

seed = 7
np.random.seed(seed)
################FEATURE-EXTRACTION############################
features_complete = np.empty((0,34))
labels_complete = np.empty((0,))



dirs = ['DC', 'JE', 'JK', 'KL']
for speaker in dirs:

    files = [file_name for file_name in os.listdir('/Users/guysimons/Documents/EmoDash/Dataset/AudioData/' + speaker) if not file_name=='.DS_Store']
    for file_name in files:
        file_path = '/Users/guysimons/Documents/EmoDash/Dataset/AudioData/' + speaker + '/' + file_name
        [Fs, x] = audioBasicIO.readAudioFile(file_path)
        features = audioFeatureExtraction.stFeatureExtraction(x, Fs, 0.05*Fs, 0.025*Fs)
        features = np.mean(features, axis=1)
        features = np.asarray(features).reshape(len(features),-1).transpose()
        features_complete = np.append(features_complete, features, axis=0)

        output_label = [re.search('^[a-z]+', file_name).group(0)]
        output_label = np.asarray(output_label) 
        labels_complete = np.append(labels_complete, output_label, axis=0)


labels_invert = {'a':0, 'd':1, 'f':2, 'h':3, 'n':4, 'sa':5, 'su':6 }

for i in range(0, labels_complete.shape[0]):
    for key in labels_invert:
        if labels_complete[i] == key:
            labels_complete[i] = labels_invert[key]

labels_complete = labels_complete.astype(int)

X = features_complete
Y = labels_complete

################PREPROCESSING############################

from sklearn.model_selection import train_test_split

X_train, X_test, y_train, y_test = train_test_split(X,Y, test_size = 0.2, random_state = 0)

from sklearn.preprocessing import StandardScaler
Sc_X = StandardScaler(with_mean = True, with_std=True)
X_train=Sc_X.fit_transform(X_train)
X_test=Sc_X.transform(X_test)

joblib.dump(Sc_X, 'featuresScaled.pkl')

dummy_y_train = np_utils.to_categorical(y_train)



################MODEL BUILDING############################



def baseline_model(optimizer = 'adam', init='normal',units=70, prop=0.3):
	# create model
	model = Sequential()
	model.add(Dense(input_dim=34, output_dim = units, kernel_initializer=init, activation='relu'))
        model.add(Dropout(prop))
	model.add(Dense(input_dim = units, output_dim = 7, kernel_initializer=init, activation='softmax'))
	
	model.compile(loss='categorical_crossentropy', optimizer=optimizer, metrics=['accuracy'])
	return model

################CROSS-VALIDATION SCORE############################
classifier = KerasClassifier(build_fn=baseline_model, verbose=0, batch_size=10, epochs=90)
kfold = KFold(n_splits=10, shuffle=True, random_state=seed)
results = cross_val_score(classifier, X_train, dummy_y_train, cv=kfold, n_jobs=-1)
print("Baseline: %.2f%% (%.2f%%)" % (results.mean()*100, results.std()*100))

################OPTIMIZATION############################
epochs = [90,100, 120]
units = [50, 70,80, 90,100]
props = [0, 0.01, 0.05, 0.2, 0.3]
optimizer = ['adam', 'rmsprop']
inits = ['normal', 'uniform']
param_grid = dict(epochs = epochs, units = units, prop = props, optimizer=optimizer, init = inits)

from sklearn.model_selection import GridSearchCV

grid = GridSearchCV(estimator = classifier, param_grid = param_grid, n_jobs=-1)
grid_result = grid.fit(X_train, dummy_y_train)
grid_result.best_score_
grid_result.best_params_

########Predict y##############
classifier.fit(X_train, dummy_y_train)
y_pred=classifier.predict(X_test)

from sklearn.metrics import accuracy_score
accuracy_score(y_test, y_pred)

classifier.score(X_train, dummy_y_train)

"""
Final Scores:
    10-Fold Cross-validation accuracy on training set: 62%
    training set accuracy: 98%
    test-set accuracy: 65%
"""
#######Save model#############
def save_model(model):
    # saving model
    json_model = model.to_json()
    open('EmoDashANN_model_v1.json', 'w').write(json_model)
    # saving weights
    model.save_weights('EmoDashANN_weights_v1.h5', overwrite=True)

model = baseline_model(optimizer = 'adam', init='normal',units=70, prop=0.3)
model.fit(X_train, dummy_y_train, nb_epoch=90, batch_size=10, verbose=1)
save_model(model)