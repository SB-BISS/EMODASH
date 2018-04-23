import sys
from sys import byteorder
from array import array
from struct import pack
import time
import numpy as np
import pyaudio
import wave
import os
import audioop
from pydub import AudioSegment

CHANNELS = 2
THRESHOLD = 100
CHUNK_SIZE = 1024
FORMAT = pyaudio.paInt16
RATE = 8000
RECORD_SECONDS = 15
WAVE_OUTPUT_FILENAME_EXTENSION = 0
WAVE_OUTPUT_FILENAME = "output"

def is_silent(snd_data):
    "Returns 'True' if below the 'silent' threshold"
    return max(snd_data) < THRESHOLD


def normalize(snd_data):
    "Average the volume out"
    MAXIMUM = 16384
    times = float(MAXIMUM) / max(abs(i) for i in snd_data)

    r = array('h')
    for i in snd_data:
        r.append(int(i * times))
    return r


def trim(snd_data):
    "Trim the blank spots at the start and end"

    def _trim(snd_data):
        snd_started = False
        r = array('h')

        for i in snd_data:
            if not snd_started and abs(i) > THRESHOLD:
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


def add_silence(snd_data, seconds):
    "Add silence to the start and end of 'snd_data' of length 'seconds' (float)"
    r = array('h', [0 for i in range(int(seconds * RATE))])
    r.extend(snd_data)
    r.extend([0 for i in range(int(seconds * RATE))])
    return r


def record():
    """
    Record a word or words from the microphone and
    return the data as an array of signed shorts.

    Normalizes the audio, trims silence from the
    start and end.
    """
    p = pyaudio.PyAudio()
    stream = p.open(format=FORMAT, channels=CHANNELS, rate=RATE, input=True, output=True, frames_per_buffer=CHUNK_SIZE)

    num_silent = 0
    snd_started = False

    r = array('h')
    count = 0
    for i in range(0, int(RATE / CHUNK_SIZE * RECORD_SECONDS)):
        count += 1
        # little endian, signed short
        snd_data = array('h', stream.read(CHUNK_SIZE))
        if byteorder == 'big':
            snd_data.byteswap()
        r.extend(snd_data)

        # print('\r%08d' % count)
        # silent = is_silent(snd_data)

        # if silent and snd_started:
        # num_silent += 1
        # elif not silent and not snd_started:
        # snd_started = True

    sample_width = p.get_sample_size(FORMAT)
    stream.stop_stream()
    stream.close()
    p.terminate()

    r = normalize(r)
    # r = trim(r)
    # r = add_silence(r, 0.5)
    return sample_width, r


def record_to_file():
        WAVE_OUTPUT_FILENAME_EXTENSION = 0
        WAVE_OUTPUT_FILENAME = "rec"
        d = True

        ts = time.time()
        EXPORT_FOLDER = "RECORDINGS_" + str(ts).split(".")[0]
        if not os.path.exists(EXPORT_FOLDER):
            os.makedirs(EXPORT_FOLDER)

        # the sound of each 3 seconds intervall
        # they get combined later to a 9 seconds total interval
        first_recording = None
        second_recording = None
        third_recording = None

        sample_width, data = record()
        # if there was no recording done so far
        # store the first 3 seconds in the first recording
        #if first_recording == None:
        first_recording = data
        # if there was only one recording done so far
        # store the next recording in the second recording
        #elif second_recording == None:
        #    second_recording = data
        # for every recording coming after the first 2 times 3 seconds
        # store the recording in the third recording
        #else:
        #    third_recording = data

            # append all the recordings to a 9 seconds interval
        data = first_recording
            #data = np.append(data, second_recording)
            #data = np.append(data, third_recording)
            # pack the data properly to be exported as a wave file
        data = pack('<' + ('h' * len(data)), *data)

        wf = wave.open(
            EXPORT_FOLDER + "/" + WAVE_OUTPUT_FILENAME + "_" + str(WAVE_OUTPUT_FILENAME_EXTENSION) + ".wav",
            'wb')
        wf.setnchannels(CHANNELS)
        wf.setsampwidth(sample_width)
        wf.setframerate(RATE)
        wf.writeframes(data)
        wf.close()

        #result = em.split_single_song(song)

        #    os.remove(
        #        EXPORT_FOLDER + "/" + WAVE_OUTPUT_FILENAME + "_" + str(WAVE_OUTPUT_FILENAME_EXTENSION) + ".wav")
        #    os.remove(
        #        EXPORT_FOLDER + "/" + WAVE_OUTPUT_FILENAME + "_" + str(WAVE_OUTPUT_FILENAME_EXTENSION) + ".mp3")

            # dict_to_append = result.to_dict('record')

            # to_json.append(dict_to_append[0])
            # print result.to_dict('list')

        # print result_all.to_json()

        # increase the name counter of the filename
        WAVE_OUTPUT_FILENAME_EXTENSION += 1

        # shift the recordings and delete the last recording
        # shift the second recording to be the first now
        first_recording = None
        first_recording = second_recording
        # shift the third recording to be the second now
        second_recording = None
        second_recording = third_recording
        # empty the third recording so a new recording can be made
        third_recording = None

        return data,sample_width


def mul_stereo(sample, width):
    lsample = audioop.tomono(sample, width, 1, 0)
    rsample = audioop.tomono(sample, width, 0, 1)
    return lsample, rsample


if __name__ == '__main__':
    data,sample_width = record_to_file()
    left, right = mul_stereo(data, sample_width)
    print type(left)
    print type(right)


    if not os.path.exists('out'):
        os.makedirs("out")

    lwf = wave.open('out/left.wav','wb')
    rwf = wave.open('out/right.wav','wb')
    lwf.setnchannels(1)
    lwf.setsampwidth(sample_width)
    lwf.setframerate(RATE)
    lwf.writeframes(left)
    lwf.close()
    rwf.setnchannels(1)
    rwf.setsampwidth(sample_width)
    rwf.setframerate(RATE)
    rwf.writeframes(right)
    rwf.close()
