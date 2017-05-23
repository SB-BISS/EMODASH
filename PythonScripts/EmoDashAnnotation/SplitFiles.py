#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Thu May 18 13:43:50 2017

@author: guysimons
"""
from pydub import AudioSegment
import numpy as np
import os
import re

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
            filepath = '/Users/guysimons/Documents/BISS/EmoDash/Development/Resources/windowDirectory/' + filename + '_window_'+ str(cntr) +'.wav'
            window.export(filepath, format = 'wav')   
            #window_names.append(filename + '_window_'+ str(cntr) +'.wav')
            break

        window = audiofile[window_index[i]:window_index[i+1]]
        filepath = '/Users/guysimons/Documents/BISS/EmoDash/Development/Resources/windowDirectory/' + filename + '_window_'+ str(cntr) +'.wav'
        window.export(filepath, format = 'wav')
        #window_names.append(filename + '_window_'+ str(cntr) +'.wav')
    #return window_names
        
def splitAllFiles(raw_files_directory, window_storage_directory):
    filenames = [name for name in os.listdir(raw_files_directory) if not name == '.DS_Store']
    for filename in filenames:
        splittingSingleFile(raw_files_directory + "/" + filename, window_storage_directory)
        
        
raw_files_directory = str(raw_input("Please specify the directory with raw files: \n"))
window_storage_directory = str(raw_input("Please specify the directory to store the splitted files: \n"))

splitAllFiles(raw_files_directory, window_storage_directory)
