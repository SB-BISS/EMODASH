#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Thu Apr 27 16:35:04 2017

@author: guysimons
"""
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

seed = 7
np.random.seed(seed)
############################################
features_complete = np.empty((0,34))
labels_complete = np.empty((0,))



dirs = ['DC', 'JE', 'JK', 'KL']
for speaker in dirs:

    files = [file_name for file_name in os.listdir('/Users/guysimons/Documents/EmoDash/Dataset/AudioData/' + speaker)]
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

#Replacing the str values with integers to indicate categories in the labels_complete array
labels_invert = {'a':0, 'd':1, 'f':2, 'h':3, 'n':4, 'sa':5, 'su':6 }

for i in range(0, labels_complete.shape[0]):
    for key in labels_invert:
        if labels_complete[i] == key:
            labels_complete[i] = labels_invert[key]

labels_complete = labels_complete.astype(int)

X = features_complete
Y = labels_complete



from sklearn.model_selection import train_test_split

X_train, X_test, y_train, y_test = train_test_split(X,Y, test_size = 0.2, random_state = 0)

from sklearn.preprocessing import StandardScaler
Sc_X = StandardScaler(with_mean = True, with_std=True)
X_train=Sc_X.fit_transform(X_train)
X_test=Sc_X.transform(X_test)

##################Linear SVM##########

from sklearn.model_selection import cross_val_score, KFold
from sklearn.metrics import accuracy_score

from sklearn.svm import SVC
classifier_linear_svm = SVC(kernel='linear', random_state=0)
classifier_linear_svm.fit(X_train, y_train)

kfold= KFold(n_splits=10, shuffle=True)
results_linear_SVM = cross_val_score(classifier_linear_svm, X_train, y_train, cv=kfold, n_jobs=-1)
print("Cross-validation linear SVM training set: %.2f" % np.mean(results_linear_SVM))


y_pred_linear_SVM = classifier_linear_svm.predict(X_test)
accuracy_score(y_test, y_pred_linear_SVM, normalize=True)

"""
Final scores:
    10-fold cross-validation accuracy on training set: 56%
    test-set accuracy: 60.4%
    
"""

##################Logistic Classifier######
from sklearn.linear_model import LogisticRegression
classifier_log_regression = LogisticRegression(penalty='l2', C=0.05)
classifier_log_regression.fit(X_train, y_train)

kfold= KFold(n_splits=10, shuffle=True)
results_log_regression = cross_val_score(classifier_log_regression, X_train, y_train, cv=kfold, n_jobs=-1)
print("Cross-validation logistic Regression training set: %.2f" % np.mean(results_log_regression))

y_pred_log_regression = classifier_log_regression.predict(X_test)
accuracy_score(y_test, y_pred_log_regression, normalize=True)

"""
Final scores:
    10-fold cross-validation accuracy on training set: 51%
    test-set accuracy: 57.3%
    
"""

##################Kernel SVM##########

classifier_kernel_svm = SVC(kernel='rbf', random_state=0)
classifier_kernel_svm.fit(X_train, y_train)

kfold= KFold(n_splits=10, shuffle=True)
results_kernel_SVM = cross_val_score(classifier_kernel_svm, X_train, y_train, cv=kfold, n_jobs=-1)
print("Cross-validation kernel SVM training set: %.2f" % np.mean(results_kernel_SVM))


y_pred_kernel_SVM = classifier_kernel_svm.predict(X_test)
accuracy_score(y_test, y_pred_kernel_SVM, normalize=True)

"""
Final scores:
    10-fold cross-validation accuracy on training set: 56%
    test-set accuracy: 62.5%
    
"""

############KNN###############
from sklearn.neighbors import KNeighborsClassifier
classifier_KNN = KNeighborsClassifier(n_neighbors = 5)
classifier_KNN.fit(X_train, y_train)

kfold= KFold(n_splits=10, shuffle=True)
results_KNN = cross_val_score(classifier_KNN, X_train, y_train, n_jobs=-1, cv=kfold)
print("Cross-validation KNN training set: %.2f" % np.mean(results_KNN))

y_pred_KNN = classifier_KNN.predict(X_test)
accuracy_score(y_test, y_pred_KNN, normalize=True)

"""
Final scores:
    10-fold cross-validation accuracy on training set: 49%
    test-set accuracy: 51%%
    
"""

############Naive Bayes###############
from sklearn.naive_bayes import GaussianNB
classifier_naivebayes = GaussianNB()
classifier_naivebayes.fit(X_train, y_train)

kfold= KFold(n_splits=10, shuffle=True)
results_naivebayes = cross_val_score(classifier_naivebayes, X_train, y_train, n_jobs=-1, cv=kfold)
print("Cross-validation Naive Bayes training set: %.2f" % np.mean(results_naivebayes))

y_pred_naivebayes = classifier_naivebayes.predict(X_test)
accuracy_score(y_test, y_pred_naivebayes, normalize=True)

"""
Final scores:
    10-fold cross-validation accuracy on training set: 50%
    test-set accuracy: 57.3%
    
"""

############Random Forests###############
from sklearn.ensemble import RandomForestClassifier
classifier_random_forests = RandomForestClassifier(n_estimators=1000, criterion='entropy', n_jobs=-1)
classifier_random_forests.fit(X_train, y_train)

kfold= KFold(n_splits=10, shuffle=True)
results_random_forests = cross_val_score(classifier_random_forests, X_train, y_train, n_jobs=-1, cv=kfold)
print("Cross-validation random forests training set: %.2f" % np.mean(results_random_forests))

y_pred_random_forests = classifier_random_forests.predict(X_test)
accuracy_score(y_test, y_pred_random_forests, normalize=True)

"""
Final scores:
    10-fold cross-validation accuracy on training set: 54%
    test-set accuracy: 65.6%
    
"""
