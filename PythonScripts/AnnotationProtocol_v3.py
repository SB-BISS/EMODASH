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
from keras.models import model_from_json
import os
import pyaudio  
import wave  
import re

#############SPLITTING FILE INTO 3 SECOND WINDOWS##############
def splitting(filepath, window_storage_directory):
    audiofile = AudioSegment.from_wav(filepath)
    duration = audiofile.duration_seconds
    window_index = np.arange(start=0,stop=duration*1000, step = 3000)
    cntr = 0
    filename = re.search('[a-zA-Z]+.wav$', filepath).group(0)
    
    for i in range(0, int(np.ceil(duration/3))):
        cntr = cntr+1
        if i == int(np.ceil(duration/3)-1.0):
            window = audiofile[window_index[i]:]
            filepath = '/Users/guysimons/Documents/EmoDash/windowDirectory/' + filename + '_window_'+ str(cntr) +'.wav'
            window.export(filepath, format = 'wav')         
            break

        window = audiofile[window_index[i]:window_index[i+1]]
        filepath = '/Users/guysimons/Documents/EmoDash/windowDirectory/' + filename + '_window_'+ str(cntr) +'.wav'
        window.export(filepath, format = 'wav')
        

"""
1. Open file
2. Measure duration of file in seconds & generate sequence of milliseconds from 0 to the duration of the file
    with a step size of 3 seconds (3000 milliseconds). This sequence will be used to split the audiofile in 3
    second windows. 
3. Split the audio file into 3-second segments by using the generated sequence
3. Save each 3-second window as a wav file in the specified directory
Note:
    The if-statement makes sure that the last few seconds at the end of the file are saved into a window of <3 seconds
    as well. 
"""

#############FEATURE-EXTRACTION##############
def featureExtraction(window_storage_directory):
    features_complete = np.ndarray((0,34))
    files = [file_name for file_name in os.listdir(window_storage_directory) if not file_name=='.DS_Store']
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

"""
1. open file
2. configure stream
3. play stream
"""

#############RECONSTRUCT MODEL##############
def construct_model(filepath_model, filepath_weights):
    
    json_file = open(filepath_model, 'r')
    loaded_model_json = json_file.read()
    json_file.close()
    loaded_model = model_from_json(loaded_model_json)
    loaded_model.load_weights(filepath_weights)
    loaded_model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])
    return loaded_model

"""
1. open json file
2. load model typology
3. load weights
4. recompile model
5. return model
"""

#############EVALUATION##############
def evaluation_model(model, features, filenames, window_storage_directory):
    features = np.asarray(features).reshape(len(features),-1)
    labels = {0:'angry', 1:'disgust', 2:'fear',3:'happiness', 4:'neutral', 5:'sadness', 6:'surprise'}
    targetLabels = []
    y_predComplete = np.ndarray((0,7))
    
    for i in range(0, features.shape[0]):
        y_pred = model.predict(np.asarray(features[i,]).reshape(1,34))
        y_predComplete = np.append(y_predComplete, y_pred, axis=0)
        result = np.argmax(y_pred)
        
        for key in labels:
            if result == key:
                emotion = labels[key]
            
        playFile(window_storage_directory + filenames[i])
        
        print("\n" + "Predicted emotion: "+ emotion)
        feedback = raw_input("Is this prediction correct for file " + filenames[i]+ "? [y/n]: \n")
        
        if feedback == 'y':
            targetLabels.append(result)
        elif feedback == 'n':
            correction = raw_input("What is the actual emotion? [0:'angry', 1:'disgust', 2:'fear',3:'happiness', 4:'neutral', 5:'sadness', 6:'surprise'] : \n")
            targetLabels.append(correction)
            
        else:
            print("Something went wrong, please follow the instructions")
    
    return targetLabels, y_predComplete

"""
1. make sure that the shape of the input vector is correct
2. predict emotion
3. transform predicted outcome class to emotion name using the labels dictionary
4. play window
5. check whether predicted emotion is correct, and if so, append prediction to targetLabels
6. if the prediction is not correct, ask for correction & append
"""
#############EXECUTION: SPLITTING FILE & RECOMPILE MODEL##############
filepath = '/Users/guysimons/Documents/EmoDash/GoogleSpeechAPI/testSentence.wav'
window_storage_directory = '/Users/guysimons/Documents/EmoDash/windowDirectory/'

splitting(filepath, window_storage_directory)
classifier = construct_model('/Users/guysimons/Documents/EmoDash/EmoDashRepo/EMODASH/PythonScripts/models/EmoDashANN_model_v1.json',
                             '/Users/guysimons/Documents/EmoDash/EmoDashRepo/EMODASH/PythonScripts/models/EmoDashANN_weights_v1.h5')

#############EXECUTION: SAVE FEATURES AND (CORRECTED) TARGET EMOTIONS##############
features, filenames = featureExtraction(window_storage_directory)
targets, y_pred = evaluation_model(classifier,features,filenames,window_storage_directory)
