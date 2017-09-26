#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Mon May 29 13:29:04 2017

@author: guysimons
"""

import os
from flask import Flask, request, render_template, redirect, send_from_directory
from werkzeug.utils import secure_filename
from pyAudioAnalysis import audioBasicIO
from pyAudioAnalysis import audioFeatureExtraction
import numpy as np
import csv
from keras.models import model_from_json
from sklearn.externals import joblib
from pydub import AudioSegment

############SPLIT FILES FUNCTION##################
def splitAudioFiles(raw_files_directory, window_storage_directory):
        filenames = [name for name in os.listdir(raw_files_directory) if not name == '.DS_Store']
        for filename in filenames:
            audiofile = AudioSegment.from_wav(os.path.join(raw_files_directory,  filename))
            duration = audiofile.duration_seconds
            window_index = np.arange(start=0,stop=duration*1000, step = 3000)
            cntr = 0

            for i in range(0, int(np.ceil(duration/3))):
                cntr = cntr+1
                if i == int(np.ceil(duration/3)-1.0):
                    window = audiofile[window_index[i]:]
                    filepath = os.path.join(window_storage_directory, filename + '_window_'+ str(cntr) +'.wav')
                    window.export(filepath, format = 'wav')   
                    break
        
                window = audiofile[window_index[i]:window_index[i+1]]
                filepath = os.path.join(window_storage_directory, filename + '_window_'+ str(cntr) +'.wav')
                window.export(filepath, format = 'wav')

############DEFINE FEATURE EXTRACTOR & MODEL##################
def featureExtraction(file_path):
        
        
        [Fs, x] = audioBasicIO.readAudioFile(file_path)
        features = audioFeatureExtraction.stFeatureExtraction(x, Fs, 0.05*Fs, 0.025*Fs)
        if (len(features)==0 or features.shape[1]<50):
            features = 'none'
        else:
            features = np.mean(features, axis=1)
            features = np.asarray(features).reshape(len(features),-1).transpose()
        
        
        return features

def constructModel(filepath_model, filepath_weights):
        
    json_file = open(filepath_model, 'r')
    loaded_model_json = json_file.read()
    json_file.close()
    loaded_model = model_from_json(loaded_model_json)
    loaded_model.load_weights(filepath_weights)
    loaded_model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])
    return loaded_model

############DEFINE WEB APP VARIABLES##################
app = Flask(__name__)

app.config['UPLOAD_FOLDER'] = '/app/static/Resources/uploads/'
app.config['windowDirectory'] = '/app/static/Resources/windowDirectory/'
app.config['LOG'] = "/app/static/Resources/EmoDashLog.txt"
app.config['ANN_MODEL'] = "/app/static/Resources/EmoDashANN_model_v1.json"
app.config['ANN_WEIGHTS'] = "/app/static/Resources/EmoDashANN_weights_v1.h5"
app.config['SCALER'] = "/app/static/Resources/featuresScaled.pkl"
app.config['OUTPUT_FEATURES'] = "/app/static/Resources/features.csv"
app.config['OUTPUT_TARGETS'] = "/app/static/Resources/targets.csv"
app.config['ALLOWED_EXTENSIONS'] = set(['wav'])
app.config['SECRET_KEY']='#1993#EmoDashWebApp'

############LANDING PAGE & INSTRUCTIONS##################
@app.route("/")
def index():
    return render_template("main.html")

@app.route("/instructions")
def instructions():
    return render_template("instructions.html")

############SPLIT FILES##################
@app.route('/splitFiles')
def splitFiles():
    return render_template("splitFiles.html")

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in app.config['ALLOWED_EXTENSIONS']

@app.route('/upload', methods=['POST'])
def upload():
    file = request.files['file']
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))   
        return render_template("splitFiles.html")

@app.route('/split')
def split():
    splitAudioFiles(app.config['UPLOAD_FOLDER'], app.config['windowDirectory'])
    return render_template("splitFiles.html")

############ANNOTATION##################
@app.route('/audioAnnotation')
def audioAnnotationPage():
    
    with open(app.config["LOG"], "r") as log:
        logfile = log.read()
        log.close()
        
    filenames = [name for name in os.listdir(app.config["windowDirectory"]) if not name in logfile]
    return render_template('audioAnnotation.html', filenames = filenames)

@app.route('/audioAnnotation/<filename>')
def evaluation(filename):
    features = featureExtraction(os.path.join(app.config['windowDirectory'], filename))
    if (features=='none'):
        with open(app.config['LOG'], "a") as log:
            log.write(filename + "\n")
            log.close()
        return redirect('/audioAnnotation')
    else:
        ANNmodel = constructModel(app.config['ANN_MODEL'], app.config['ANN_WEIGHTS'])
        features_ns = np.asarray(features).reshape(len(features),-1)
        featureScaler = joblib.load(app.config['SCALER'])
        features = featureScaler.transform(features_ns)
        labels = {0:'angry', 1:'disgust', 2:'fear',3:'happiness', 4:'neutral', 5:'sadness', 6:'surprise'}
        y_pred = ANNmodel.predict(np.asarray(features).reshape(1,34))
        result = np.argmax(y_pred)
        
        for key in labels:
                if result == key:
                    emotion = labels[key]
          
        with open(app.config['OUTPUT_FEATURES'], 'a') as f:
            w_f = csv.writer(f)
            w_f.writerow([filename ,features[0,0],features[0,1],features[0,2],features[0,3],features[0,4],features[0,5],features[0,6],features[0,7]
            ,features[0,8],features[0,9],features[0,10],features[0,11],features[0,12],features[0,13],features[0,14],features[0,15],features[0,16],
            features[0,17],features[0,18],features[0,19],features[0,20],features[0,21],features[0,22],features[0,23],features[0,24],features[0,25],
            features[0,26],features[0,27],features[0,28],features[0,29],features[0,30],features[0,31],features[0,32],features[0,33]])
        
        with open(app.config['LOG'], "a") as log:
            log.write(filename + "\n")
            log.close()

        return render_template('evaluation.html', filename = filename, prediction = emotion)


@app.route('/submitForm', methods=['POST'])
def writeTarget():
    target = request.form['emotion']
    
    with open(app.config['OUTPUT_TARGETS'], 'a') as t:
        w_t = csv.writer(t)
        w_t.writerow(target)
    

    return redirect('/audioAnnotation')

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0')


