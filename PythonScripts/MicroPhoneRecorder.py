
import sys
from sys import byteorder
from array import array
from struct import pack
import time
import threading
from Queue import Queue
import numpy as np
import pyaudio
import wave
import os
from pydub import AudioSegment
import FeatureExtractor
import requests


class MicroPhoneRecorder:


    def __init__(self,Device = 1, Input = True, Channels = 1,  THRESHOLD = 500, CHUNK_SIZE = 1024, FORMAT = pyaudio.paInt16, RATE = 8000, RECORD_SECONDS = 3,WAVE_OUTPUT_FILENAME_EXTENSION = 0, EXPORT_FOLDER= "Recordings", WAVE_OUTPUT_FILENAME = "output", BASELINE = 'baseline_mean_sd.pickle'):

        self.Input = Input
        self.Device = Device
        self.Channels=Channels

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
        for i in range(0, int(self.RATE / self.CHUNK_SIZE * self.RECORD_SECONDS)):
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

            d = True
            print("starting")
            ts = time.time()
            EXPORT_FOLDER = self.EXPORT_FOLDER + "_RECORDINGS_" + str(ts).split(".")[0]
            if not os.path.exists(EXPORT_FOLDER):
                os.makedirs(EXPORT_FOLDER)

            # the sound of each 3 seconds intervall
            # they get combined later to a 9 seconds total interval
            first_recording = None
            second_recording = None
            third_recording = None
            while d:
                self.q.join()

                sample_width, data = self.record()
                # if there was no recording done so far
                # store the first 3 seconds in the first recording
                if first_recording == None:
                    first_recording = data
                # if there was only one recording done so far
                # store the next recording in the second recording
                elif second_recording == None:
                    second_recording = data
                # for every recording coming after the first 2 times 3 seconds
                # store the recording in the third recording
                else:
                    third_recording = data

                    # append all the recordings to a 9 seconds interval
                    data = first_recording
                    data = np.append(data, second_recording)
                    data = np.append(data, third_recording)
                    # pack the data properly to be exported as a wave file
                    data = pack('<' + ('h' * len(data)), *data)

                    wf = wave.open(
                        EXPORT_FOLDER + "/" + self.WAVE_OUTPUT_FILENAME + "_" + str(self.WAVE_OUTPUT_FILENAME_EXTENSION) + ".wav",
                        'wb')
                    wf.setnchannels(1)
                    wf.setsampwidth(sample_width)
                    wf.setframerate(self.RATE)
                    wf.writeframes(data)
                    wf.close()

                    #
                    song = AudioSegment.from_wav(
                        EXPORT_FOLDER + "/" + self.WAVE_OUTPUT_FILENAME + "_" + str(self.WAVE_OUTPUT_FILENAME_EXTENSION) + ".wav")

                    #This has to be transformed here.

                    result =  self.fe.split_song(song) # just get the features out.

                    response = requests.post('localhost:50000', data=result)
                    print(response)

                    #                 result["filename"] = i

                    # dict_to_append = result.to_dict('record')

                    # to_json.append(dict_to_append[0])
                    # print result.to_dict('list')
                    #sys.stdout.write("\r" + str(response.to_dict('record')[0]))
                    #sys.stdout.flush()
                    # print result_all.to_json()

                    # increase the name counter of the filename
                    self.WAVE_OUTPUT_FILENAME_EXTENSION += 1

                    # shift the recordings and delete the last recording
                    # shift the second recording to be the first now
                    first_recording = None
                    first_recording = second_recording
                    # shift the third recording to be the second now
                    second_recording = None
                    second_recording = third_recording
                    # empty the third recording so a new recording can be made
                    third_recording = None

                # d = False

                # Exit the loop with enter
                try:
                    if self.q.get(timeout=0) == 1:
                        d = False
                except:
                    pass

            print('Task Completing')
            self.q.task_done()

    #if __name__ == '__main__':

    def start_recording(self):
        self.t = threading.Thread(target=self.record_to_file)
        self.t.daemon = True
        self.t.start()

    def stop_recording(self):
        self.q.put(1)
        self.q.join()
        #self.t.stop()

