#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Tue May  9 11:56:57 2017

@author: guysimons
"""
import numpy as np
from pydub import AudioSegment
from pyAudioAnalysis import audioBasicIO
from pyAudioAnalysis import audioFeatureExtraction
import os
import pyaudio  
import wave  

filepath = '/Users/guysimons/Documents/EmoDash/GoogleSpeechAPI/testSentence.wav'
window_storage_directory = '/Users/guysimons/Documents/EmoDash/windowDirectory/'
ANN_model = ''

#############SPLITTING FILE INTO 3 SECOND WINDOWS##############
def splitting(filepath = filepath, storing_directory= window_storage_directory):
    audiofile = AudioSegment.from_wav(filepath)
    first3Sec = audiofile[:3000]
    first3Sec.export('/Users/guysimons/Documents/EmoDash/GoogleSpeechAPI/first3sec.wav', format='wav')

"""
1. Open file
2. split file into 3 second windows (package: pydub)
3. generate random number to function as file name
3. store each window as wav in storage directory
"""

#############FEATURE-EXTRACTION##############
def featureExtraction(window_storage_directory = window_storage_directory):
    features_complete = np.ndarray((0,34))
    files = [file_name for file_name in os.listdir(window_storage_directory)]
    for file_name in files:
        file_path = window_storage_directory + file_name
        [Fs, x] = audioBasicIO.readAudioFile(file_path)
        features = audioFeatureExtraction.stFeatureExtraction(x, Fs, 0.05*Fs, 0.025*Fs)
        features = np.mean(features, axis=1)
        features = np.asarray(features).reshape(len(features),-1).transpose()
        features_complete = np.append(features_complete, features, axis=0)
    
    return features_complete, files

"""
1. open window/file from window storage directory
2. extract features from window
3. aggregate features & store in features_complete array
3. return features_complete array
"""

#############PLAY FILE##############        
def playFile(filepath):
    chunk = 1024  
    f = wave.open(filepath,"rb")   
    p = pyaudio.PyAudio()  
    stream = p.open(format = p.get_format_from_width(f.getsampwidth()),  
                channels = f.getnchannels(),  
                rate = f.getframerate(),  
                output = True)  

    data = f.readframes(chunk)  
 
    while data:  
        stream.write(data)  
        data = f.readframes(chunk)  

    stream.stop_stream()  
    stream.close()  
    p.terminate() 

playFile('/Users/guysimons/Documents/EmoDash/GoogleSpeechAPI/first3sec.wav')
    
    

