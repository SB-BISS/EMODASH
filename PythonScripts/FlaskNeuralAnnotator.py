from flask import Flask, request, url_for

import os
from keras.models import Sequential
from keras.layers import Dense
from keras.models import model_from_json
import numpy as np
import json
import sys
import pandas as pd

app = Flask(__name__)

import EmotionExtractor

#em = EmotionExtractor.EmotionExtractor('baseline.npy', 'baseline_mean_sd.pickle', Conv=False)
#em = EmotionExtractor.EmotionExtractor('baseline.npy', 'baseline_mean_sd.pickle', Conv=True)

em = EmotionExtractor.EmotionExtractor('baseline_context5_conv_simple.weights', 'mean_std.csv', Conv=False)

@app.route('/alive', methods= ['GET'])
def alive():
    print('Hello world!')
    return "ALIVE"


@app.route('/annotate', methods=['POST'])
def annotate():
    if request.method == 'POST':

        mydata = request.data

        Stringcodio = mydata.replace("[", "").replace("]","").split(",")
        values = [float(val) for val in Stringcodio]
        print(values)
        valpred = np.reshape(np.array(values), (5,136))
        prediction = em.predict_emotion(valpred)

        jsonpred = pd.Series(prediction).to_json(orient='values')

        return jsonpred

@app.route('/annotate2', methods=['POST'])
def annotate2():
    if request.method == 'POST':

        mydata = request.data

        Stringcodio = mydata.replace("[", "").replace("]","").split(",")
        values = [float(val) for val in Stringcodio]
        valpred = np.reshape(np.array(values), (119,34))
        prediction = em.predict_emotion(valpred)

        jsonpred = pd.Series(prediction).to_json(orient='values')

        return jsonpred



if __name__ == '__main__':
    app.run(host="0.0.0.0", port=int("45000"), debug=True)