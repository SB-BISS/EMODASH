#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Mon May 29 13:29:04 2017

@author: guysimons
"""

import os
import time
import base64
import requests
import json
from flask import Flask, request, render_template, redirect, send_from_directory
from werkzeug.utils import secure_filename
from pyAudioAnalysis import audioBasicIO
from pyAudioAnalysis import audioFeatureExtraction
import numpy as np
import csv
from pydub import AudioSegment

import pyglet

############SPLIT FILES FUNCTION##################
def splitAudioFiles(raw_files_directory, window_storage_directory):
        
        filenames = [file for file in os.listdir(raw_files_directory) if os.path.isfile(os.path.join(raw_files_directory, file))]
        
        #filenames = [name for name in os.listdir(raw_files_directory) if not name == '.DS_Store']
        for filename in filenames:
            print(os.path.join(raw_files_directory,  filename))
            audiofile = AudioSegment.from_wav(os.path.join(raw_files_directory,  filename))
            duration = audiofile.duration_seconds
            window_index = np.arange(start=0,stop=duration*1000, step = 3000)
            cntr = 0
            for i in range(0, int(np.ceil(duration/3))):
                cntr = cntr+1
                if i == int(np.ceil(duration/3)-1.0):
                    window = audiofile[window_index[i]:]
                    filepath = os.path.join(raw_files_directory+window_storage_directory, "demo" + '_window_'+ str(cntr) +'.wav')
                    window.export(filepath, format = 'wav')   
                    break
        
                window = audiofile[window_index[i]:window_index[i+1]]
                filepath = os.path.join(raw_files_directory+window_storage_directory, "demo" + '_window_'+ str(cntr) +'.wav')
                window.export(filepath, format = 'wav')


############DEFINE WEB APP VARIABLES##################


app = Flask(__name__)

app.config['UPLOAD_FOLDER_AGENT'] = 'static/agent_files/'
app.config['UPLOAD_FOLDER_CUSTOMER'] = 'static/customer_files/'
app.config['windowDirectory'] = 'windowDirectory/'
app.config['LOG'] = "/app/static/Resources/EmoDashLog.txt"
app.config['ALLOWED_EXTENSIONS'] = set(['wav'])
app.config['SECRET_KEY']='#1993#EmoDashWebApp'
app.config['url_endpoint'] = 'http://localhost:8080/'


######### delay function
def clever_function():
    time.sleep(3)
    return ""


@app.route('/PlaySound')    
def play_sound():
    
    agent_directory = app.config['UPLOAD_FOLDER_AGENT']+app.config["windowDirectory"]
    customer_directory = app.config['UPLOAD_FOLDER_CUSTOMER']+app.config["windowDirectory"]
    filenames_agent = [name for name in os.listdir(agent_directory) if os.path.isfile(os.path.join(agent_directory, name))]
    filenames_customer = [name for name in os.listdir(customer_directory) if os.path.isfile(os.path.join(customer_directory, name))]
  
    for i in range(0,len(filenames_agent)):#same length for files
        file_a = filenames_agent[i]
        music = pyglet.resource.media(agent_directory+file_a)
        music.play() #send it here too !
        file_c = filenames_customer[i]
        music2 = pyglet.resource.media(customer_directory+file_c)
        music2.play() #send it here too !
        #send the files here.
        
        in_file = open(agent_directory+file_a, "rb") # opening for [r]eading as [b]inary
        data_a = in_file.read() # if you only wanted to read 512 bytes, do .read(512)
        in_file.close()
        
        
        in_file = open(customer_directory+file_c, "rb") # opening for [r]eading as [b]inary
        data_c = in_file.read() # if you only wanted to read 512 bytes, do .read(512)
        in_file.close()
        
        dictionary_agent = {"id":"ag1","callId":"call1","wav_stream": base64.b64encode(bytearray(data_a))}
        dictionary_customer = {"id":"cus1","callId":"call1","wav_stream": base64.b64encode(bytearray(data_c))}
        
        j_agent = json.dumps(dictionary_agent)
        
        j_customer = json.dumps(dictionary_agent)
        
        print(j_customer)
        
        #it is a uggly hack to put
        post_response = requests.post(url=app.config['url_endpoint']+'post_wave_agent_string', data=j_agent)
        print(post_response)
        post_response = requests.post(url=app.config['url_endpoint']+'post_wave_customer_string', data=j_customer)
        print(post_response)
        
        clever_function() # each three seconds
        
    #pyglet.app.run()
    return render_template("main.html")



app.jinja_env.globals.update(clever_function=clever_function)
#app.jinja_env.globals.update(play_sound=play_sound)


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

@app.route('/upload_agent', methods=['POST'])
def upload_agent():
    file = request.files['file']
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER_AGENT'], filename))   
        return redirect('/split_agent')

@app.route('/upload_customer', methods=['POST'])
def upload_customer():
    file = request.files['file']
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER_CUSTOMER'], filename))   
        return redirect('/split_customer')


@app.route('/split_agent')
def split_agent():
    splitAudioFiles(app.config['UPLOAD_FOLDER_AGENT'], app.config['windowDirectory'])
    return render_template("splitFiles.html")

@app.route('/split_customer')
def split_customer():
    splitAudioFiles(app.config['UPLOAD_FOLDER_CUSTOMER'], app.config['windowDirectory'])
    return redirect("/PlayFiles")
    
    
@app.route('/PlayFiles')    
def play_files():   
    agent_directory = app.config['UPLOAD_FOLDER_AGENT']+app.config["windowDirectory"]
    customer_directory = app.config['UPLOAD_FOLDER_CUSTOMER']+app.config["windowDirectory"]
    filenames_agent = [name for name in os.listdir(agent_directory) if os.path.isfile(os.path.join(agent_directory, name))]
    filenames_customer = [name for name in os.listdir(customer_directory) if os.path.isfile(os.path.join(customer_directory, name))]
    return render_template("PlayFiles.html", filenames_agent = filenames_agent, filenames_customer = filenames_customer)


############ANNOTATION##################
@app.route('/audioAnnotation')
def audioAnnotationPage():
    
    with open(app.config["LOG"], "r") as log:
        logfile = log.read()
        log.close()
        
    filenames = [name for name in os.listdir(app.config["windowDirectory"]) if not name in logfile]
    return render_template('audioAnnotation.html', filenames = filenames)


if __name__ == "__main__":
    app.run(debug=True,port=int("50001"), host='0.0.0.0')


