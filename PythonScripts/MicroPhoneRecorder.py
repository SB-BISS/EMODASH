import audioop
import os
import threading
import time
import traceback
import wave
from Queue import Queue
from array import array
from collections import deque
from struct import pack
from sys import byteorder
import time
from StringIO import StringIO
import datetime
import numpy as np
import pandas as pd
import pyaudio
import threading
import requests
from pydub import AudioSegment
from pymongo import MongoClient

import FeatureExtractor
from ObjectWithEvents import ObjectWithEvents

class MicroPhoneRecorder(ObjectWithEvents):

    def __init__(self,Device = 1, Input = True, Channels = 2,  THRESHOLD = 500, CHUNK_SIZE = 1024, FORMAT = pyaudio.paInt16, RATE = 8000, RECORD_SECONDS = 3.25,WAVE_OUTPUT_FILENAME_EXTENSION = 0, EXPORT_FOLDER= "Recordings", WAVE_OUTPUT_FILENAME = "output", BASELINE = 'baseline_mean_sd.pickle', URL= "http://localhost:50000/annotate"):
        self.myqueue= deque([])
        self.Input = Input
        self.Device = Device
        self.Channels=Channels
        self.URL = URL

        if (Input==False):
            self.Output = True
            self.Channels = 0

        self.THRESHOLD = THRESHOLD
        self.EXPORT_FOLDER = EXPORT_FOLDER
        self.CHUNK_SIZE = CHUNK_SIZE
        self.FORMAT = FORMAT
        self.RATE = RATE
        self.RECORD_SECONDS = RECORD_SECONDS
        self.WAVE_OUTPUT_FILENAME_EXTENSION = WAVE_OUTPUT_FILENAME_EXTENSION
        self.WAVE_OUTPUT_FILENAME = WAVE_OUTPUT_FILENAME
        self.q = Queue()
        self.lock = threading.Lock()
        self.stopRecordingEvent = None
        self.fe = FeatureExtractor.FeatureExtractor(BASELINE)

    def is_silent(self,snd_data):
        "Returns 'True' if below the 'silent' threshold"
        return max(snd_data) < self.THRESHOLD

    def normalize(self,snd_data):
        "Average the volume out"
        MAXIMUM = 16384
        times = float(MAXIMUM) / max(abs(i) for i in snd_data)

        r = array('h')
        for i in snd_data:
            r.append(int(i * times))
        return r

    def trim(self,snd_data):
        "Trim the blank spots at the start and end"

        def _trim(snd_data):
            snd_started = False
            r = array('h')

            for i in snd_data:
                if not snd_started and abs(i) > self.THRESHOLD:
                    snd_started = True
                    r.append(i)

                elif snd_started:
                    r.append(i)
            return r

        # Trim to the left
        snd_data = _trim(snd_data)

        # Trim to the right
        snd_data.reverse()
        snd_data = _trim(snd_data)
        snd_data.reverse()
        return snd_data


    def add_silence(self,snd_data, seconds):
        "Add silence to the start and end of 'snd_data' of length 'seconds' (float)"
        r = array('h', [0 for i in range(int(seconds * self.RATE))])
        r.extend(snd_data)
        r.extend([0 for i in range(int(seconds * self.RATE))])
        return r


    def record(self):
        """
        Record a word or words from the microphone and
        return the data as an array of signed shorts.

        Normalizes the audio, trims silence from the
        start and end.
        """
        p = pyaudio.PyAudio()
        if self.Input==True:
            stream = p.open(format=self.FORMAT, channels=self.Channels, input_device_index=self.Device , rate=self.RATE, input=True, frames_per_buffer=self.CHUNK_SIZE)
        else:
            stream = p.open(format=self.FORMAT, channels=self.Channels, output_device_index=self.Device, rate=self.RATE,
                            input=False, output=True, frames_per_buffer=self.CHUNK_SIZE)

        num_silent = 0
        snd_started = False

        r = array('h')
        count = 0
        for i in range(0, int(self.RATE / self.CHUNK_SIZE * (self.RECORD_SECONDS))):
            count += 1
            # little endian, signed short
            snd_data = array('h', stream.read(self.CHUNK_SIZE))
            if byteorder == 'big':
                snd_data.byteswap()
            r.extend(snd_data)

            # print('\r%08d' % count)
            # silent = is_silent(snd_data)

            # if silent and snd_started:
            # num_silent += 1
            # elif not silent and not snd_started:
            # snd_started = True

        sample_width = p.get_sample_size(self.FORMAT)
        stream.stop_stream()
        stream.close()
        p.terminate()

        r = self.normalize(r)
        # r = trim(r)
        # r = add_silence(r, 0.5)
        return sample_width, r


    def record_to_file(self):
        with self.lock:

            print("starting")

            numInitIntervals = 5 # model needs a recording of 5 sound samples of 3 seconds
            recording = np.array([], 'h')

            while not self.stopRecordingEvent.isSet(): # while we are recoding the call

                try:
                    # record sound sample of 3 seconds
                    sample_width, data = self.record()

                    # add new 3 second sample to back of recording
                    recording = np.append(recording, data) 
                  
                    dataLength = len(data)

                    if (len(recording) == numInitIntervals * dataLength):
                        # start new thread to process the latest 5 x 3 seconds recording
                        threading.Thread(name='preprocessor', target=self.process_data, args=(recording, sample_width)).start()
                        # slice oldest 3 seconds sample from front of recording
                        recording = recording[dataLength:]

                except Exception, e:
                    traceback.print_exc()
                    print("Exception in Processing Audio. Continuing..." + str(e))
                    pass

            print('Recording stopped')


    def process_data(self,data,sample_width):

        splitchannel_start_time = time.time()

        data = pack('<' + ('h' * len(data)), *data)
        data_L, data_R = self.mul_stereo(data, sample_width)

        splitchannel_duration = time.time() - splitchannel_start_time

        feature_start_time = time.time()

        song_L = AudioSegment.from_file(StringIO(data_L), format="raw", channels=1, sample_width=sample_width, frame_rate=self.RATE)
        song_R = AudioSegment.from_file(StringIO(data_R), format="raw", channels=1, sample_width=sample_width, frame_rate=self.RATE)

        # This has to be transformed here.

        result_L = self.fe.split_song(song_L)  # just get the features out.
        result_R = self.fe.split_song(song_R)  # just get the features out.

        feature_duration = time.time() - feature_start_time

        analysis_start_time = time.time()

        headers = {'Content-Type': 'application/json', 'Accept': 'application/json'}

        var_res_L = pd.Series(result_L).to_json(orient='values')
        var_res_R = pd.Series(result_R).to_json(orient='values')

        start_time = time.time()
        response_L = requests.post(self.URL, headers=headers, data=var_res_L)
        response_R = requests.post(self.URL, headers=headers, data=var_res_R)

        if not self.stopRecordingEvent.isSet():
            print("--- %s seconds ---" % (time.time() - start_time))

            analysis_duration = time.time() - analysis_start_time

            duration = {"split": splitchannel_duration, "features": feature_duration, "analysis": analysis_duration}

            payload = {"duration": duration, "left_emotion": response_L.json(), "right_emotion": response_R.json(),
                                "left_features": var_res_L, "right_features": var_res_R}

            # trigger event 
            super(MicroPhoneRecorder, self).trigger('emotionsChanged', payload)

    def mul_stereo(self, sample, width):
        lsample = audioop.tomono(sample, width, 1, 0)
        rsample = audioop.tomono(sample, width, 0, 1)
        return lsample, rsample

    def start_recording(self):
        self.stopRecordingEvent = threading.Event()
        self.t = threading.Thread(target=self.record_to_file)
        self.t.daemon = True
        self.t.start()

    def stop_recording(self):
        self.stopRecordingEvent.set()


