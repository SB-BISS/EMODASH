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
import pandas as pd
from sklearn.externals import joblib

#############SPLITTING FILE INTO 3 SECOND WINDOWS##############
def splittingSingleFile(filepath, window_storage_directory):
    audiofile = AudioSegment.from_wav(filepath)
    duration = audiofile.duration_seconds
    window_index = np.arange(start=0,stop=duration*1000, step = 3000)
    cntr = 0
    filename = re.search('[a-zA-Z0-9]+.wav$', filepath).group(0)
    #window_names = []
    
    for i in range(0, int(np.ceil(duration/3))):
        cntr = cntr+1
        if i == int(np.ceil(duration/3)-1.0):
            window = audiofile[window_index[i]:]
            filepath = '/Users/guysimons/Documents/EmoDash/windowDirectory/' + filename + '_window_'+ str(cntr) +'.wav'
            window.export(filepath, format = 'wav')   
            #window_names.append(filename + '_window_'+ str(cntr) +'.wav')
            break

        window = audiofile[window_index[i]:window_index[i+1]]
        filepath = '/Users/guysimons/Documents/EmoDash/windowDirectory/' + filename + '_window_'+ str(cntr) +'.wav'
        window.export(filepath, format = 'wav')
        #window_names.append(filename + '_window_'+ str(cntr) +'.wav')
    #return window_names
        
def splitAllFiles(raw_files_directory, window_storage_directory):
    filenames = [name for name in os.listdir(raw_files_directory) if not name == '.DS_Store']
    for filename in filenames:
        splittingSingleFile(raw_files_directory + "/" + filename, window_storage_directory)
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
def featureExtraction(filename,window_storage_directory):
    
    file_path = window_storage_directory + filename
    [Fs, x] = audioBasicIO.readAudioFile(file_path)
    features = audioFeatureExtraction.stFeatureExtraction(x, Fs, 0.05*Fs, 0.025*Fs)
    if (len(features)==0 or features.shape[1]<50):
        features = 'none'
    else:
        features = np.mean(features, axis=1)
        features = np.asarray(features).reshape(len(features),-1).transpose()
    
    
    return features

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
def evaluation_model(model, features, filename, window_storage_directory, standardScaler_model_path):
    features_ns = np.asarray(features).reshape(len(features),-1)
    labels = {0:'angry', 1:'disgust', 2:'fear',3:'happiness', 4:'neutral', 5:'sadness', 6:'surprise'}
    featureScaler = joblib.load(standardScaler_model_path)
    features = featureScaler.transform(features_ns)
    
    y_pred = model.predict(np.asarray(features).reshape(1,34))
    result = np.argmax(y_pred)
    
    for key in labels:
        if result == key:
            emotion = labels[key]
    rep = True
    while rep == True:
        playFile(window_storage_directory + filename)
        
    
        print("\n" + "Predicted emotion: "+ emotion)
        feedback = raw_input("Is this prediction correct for file " + filename + "? [y/n/repeat/quit]: \n")
        
        if feedback == 'y':
            targetLabel = result
            rep = False
        elif feedback == 'n':
            correction = raw_input("What is the actual emotion? [0:'angry', 1:'disgust', 2:'fear',3:'happiness', 4:'neutral', 5:'sadness', 6:'surprise'] : \n")
            targetLabel = correction
            rep = False
        elif feedback == 'repeat':
            rep = True
        elif feedback == 'quit':
            targetLabel = 'quit'
            break
            
        else:
            print("Something went wrong, please follow the instructions")
    
    
    return targetLabel

"""
1. make sure that the shape of the input vector is correct
2. predict emotion
3. transform predicted outcome class to emotion name using the labels dictionary
4. play window
5. check whether predicted emotion is correct, and if so, append prediction to targetLabels
6. if the prediction is not correct, ask for correction & append
"""

def saveOutput(features, targets, features_path, targets_path):
    features_df = pd.DataFrame(features) 
    
    targets_df = pd.DataFrame(targets)
    
    targets_df.to_csv(targets_path)
    
    features_df.to_csv(features_path)
    

def Main(window_storage_directory, log_file_path, model,standardScaler_model_path):
    with open(log_file_path) as f:
        completed_files = f.readlines()
        completed_files = [x.strip() for x in completed_files]
        f.close()
    features_complete = np.ndarray((0,34))
    target_complete = np.ndarray((0,1))
    filenames = [file_name for file_name in os.listdir(window_storage_directory) if not file_name in completed_files]
    for filename in filenames:
        features = featureExtraction(filename, window_storage_directory)
        if features == 'none':
            continue
        target = np.asarray(evaluation_model(model, features, filename, window_storage_directory, standardScaler_model_path)).reshape((1,1))
        if target == 'quit':
            break
        features_complete = np.append(features_complete, features, axis=0)
        target_complete = np.append(target_complete, target, axis=0)
        
        with open(log_file_path, "a") as f:
            f.write(filename + '\n')
            f.close()
        
    return features_complete, target_complete
        
        

#############EXECUTION: SPLITTING FILE & RECOMPILE MODEL##############
raw_files_directory = '/Users/guysimons/Documents/EmoDash/test3'
window_storage_directory = '/Users/guysimons/Documents/EmoDash/windowDirectory/'
log_file_path = '/Users/guysimons/Documents/EmoDash/EmoDashLog.txt'
features_csv = '/Users/guysimons/Documents/EmoDash/featuresComplete.csv'
targets_csv = '/Users/guysimons/Documents/EmoDash/targetComplete.csv'
standardScaler_model = '/Users/guysimons/Documents/EmoDash/EmoDashRepo/EMODASH/PythonScripts/featuresScaled.pkl'

model = construct_model('/Users/guysimons/Documents/EmoDash/EmoDashRepo/EMODASH/PythonScripts/models/EmoDashANN_model_v1.json',
                             '/Users/guysimons/Documents/EmoDash/EmoDashRepo/EMODASH/PythonScripts/models/EmoDashANN_weights_v1.h5')


splitAllFiles(raw_files_directory, window_storage_directory)
features_complete, targets_complete = Main(window_storage_directory, log_file_path, model, standardScaler_model)


#############SAVING OUTPUT TO CSV##############
saveOutput(features_complete, targets_complete, features_csv, targets_csv)