#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Tue May  9 11:56:57 2017

@author: guysimons
"""
import numpy as np
from pyAudioAnalysis import audioBasicIO
from pyAudioAnalysis import audioFeatureExtraction
from keras.models import model_from_json
import os
import pyaudio  
import wave  
import pandas as pd
from sklearn.externals import joblib


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
    
    targets_df.to_csv(targets_path, index=False, header=False, mode = "a")
    
    features_df.to_csv(features_path, index=False, header=False, mode = "a")
    

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
        
        

#############CONFIG VARIABLES##############
window_storage_directory = str(raw_input("Please specify the directory containing the splitted files: \n"))
log_file_path = str(raw_input("Please specify the location of the log file: \n"))
features_csv = str(raw_input("Please specify the csv file to save the extracted features to: \n"))
targets_csv = str(raw_input("Please specify the csv file to save the targets to: \n"))
standardScaler_model = str(raw_input("Please specify the file containing the featuresScalar: \n"))
model_architecture = str(raw_input("Please specify the json file containing the model: "))
model_weights = str(raw_input("Please specify the file containing the model weights: "))

model = construct_model(model_architecture, model_weights)


#############EVALUATE MODEL##############
features_complete, targets_complete = Main(window_storage_directory, log_file_path, model, standardScaler_model)


#############SAVING OUTPUT TO CSV##############
saveOutput(features_complete, targets_complete, features_csv, targets_csv)
            
with open(log_file_path, "r") as f:
    log = f.readlines()
    f.close()

log = log[2:]
    