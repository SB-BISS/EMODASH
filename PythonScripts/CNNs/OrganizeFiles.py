#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jul 24 11:29:24 2017

@author: guysimons
"""

import os, shutil

original_dataset_dir = '/Users/guysimons/Documents/BISS/EmoDash/CNN_Development/Databases/SAVEE_EMODB_SPEC'

train_dir = os.path.join(original_dataset_dir, 'train')
os.mkdir(train_dir)

test_dir = os.path.join(original_dataset_dir, 'test')
os.mkdir(test_dir)

angry_dir = os.path.join(train_dir, 'angry')
os.mkdir(angry_dir)
disgust_dir = os.path.join(train_dir, 'disgust')
os.mkdir(disgust_dir)
fear_dir = os.path.join(train_dir, 'fear')
os.mkdir(fear_dir)
happy_dir = os.path.join(train_dir, 'happy')
os.mkdir(happy_dir)
neutral_dir = os.path.join(train_dir, 'neutral')
os.mkdir(neutral_dir)
sadness_dir = os.path.join(train_dir, 'sadness')
os.mkdir(sadness_dir)
surprise_dir = os.path.join(train_dir, 'surprise')
os.mkdir(surprise_dir)

angry_dir = os.path.join(test_dir, 'angry')
os.mkdir(angry_dir)
disgust_dir = os.path.join(test_dir, 'disgust')
os.mkdir(disgust_dir)
fear_dir = os.path.join(test_dir, 'fear')
os.mkdir(fear_dir)
happy_dir = os.path.join(test_dir, 'happy')
os.mkdir(happy_dir)
neutral_dir = os.path.join(test_dir, 'neutral')
os.mkdir(neutral_dir)
sadness_dir = os.path.join(test_dir, 'sadness')
os.mkdir(sadness_dir)
surprise_dir = os.path.join(test_dir, 'surprise')
os.mkdir(surprise_dir)

filenames = os.listdir(os.path.join(original_dataset_dir, 'Spectrograms'))

import random

train = random.sample(filenames, 800)
test = [i for i in filenames if not i in train]

import re

emotions_dic = {"a":"angry", "d":"disgust", "f":"fear", "h":"happy", "n":"neutral", "sa":"sadness", "su":"surprise"}

def movefiles(file ,source, target, emotion, emotion_dic):
     emotion_beginning = re.search("_[a-z]+", file).span()[0] + 1
     emotion_end = re.search("_[a-z]+", file).span()[1]
     if file[emotion_beginning:emotion_end] == emotion:
          src = os.path.join(source, file)
          dst = os.path.join(target, emotion_dic[emotion] ,file)
          shutil.copyfile(src,dst)

for file in train:
     if file == ".DS_Store":
          continue
     for emotion in emotions_dic.keys():
          movefiles(file, os.path.join(original_dataset_dir, 'Spectrograms'), os.path.join(train_dir), emotion, emotions_dic)


for file in test:
     if file == ".DS_Store":
          continue
     for emotion in emotions_dic.keys():
          movefiles(file, os.path.join(original_dataset_dir, 'Spectrograms'), os.path.join(test_dir), emotion, emotions_dic)

def countTrainingFiles(emotion):
     print("total " + emotion + " images for training: ", len(os.listdir(os.path.join("/Users/guysimons/Documents/BISS/EmoDash/CNN_Development/Databases/SAVEE_EMODB_SPEC/train", emotion))))

def countTestingFiles(emotion):
     print("total " + emotion + " images for testing: ", len(os.listdir(os.path.join("/Users/guysimons/Documents/BISS/EmoDash/CNN_Development/Databases/SAVEE_EMODB_SPEC/test", emotion))))


for emotion in emotions_dic.values():
     countTrainingFiles(emotion)
     countTestingFiles(emotion)
     
"""
Note: the total amount of files used for training/testing is less than the total files
in the SAVEE and EMO-DB databases, as the latter also contains the "boring" emotion
which the model does not take into account
"""