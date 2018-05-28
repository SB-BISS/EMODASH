from flask import Flask, request, url_for

import os
from keras.models import Sequential
from keras.layers import Dense
from keras.models import model_from_json
import numpy as np
import json
import sys
import pandas as pd
import tensorflow as tf

app = Flask(__name__)

import EmotionExtractor

#em = EmotionExtractor.EmotionExtractor('baseline.npy', 'baseline_mean_sd.pickle', Conv=False)
#em = EmotionExtractor.EmotionExtractor('baseline.npy', 'baseline_mean_sd.pickle', Conv=True)

em = EmotionExtractor.EmotionExtractor('baseline_context5_conv_simple2.weights', 'mean_std.csv', Conv=False)

graph = tf.get_default_graph()

@app.route('/alive', methods= ['GET'])
def alive():
    print('Hello world!')
    return "ALIVE"

""" endpoint for target verification Loader.io """
@app.route('/loaderio-c2146f3353da3bd1786e4233a8de669a/', methods=['GET'])
def loaderio():
    return 'loaderio-c2146f3353da3bd1786e4233a8de669a'

@app.route('/loaderio-c59890271e009cafd5ad3fd5c5a3f542/', methods=['GET'])
def loaderio2():
    return 'loaderio-c59890271e009cafd5ad3fd5c5a3f542'


@app.route('/annotate', methods=['POST'])
def annotate():
    if request.method == 'POST':

        mydata = request.data
        Stringcodio = mydata.decode('utf_8').replace("[", "").replace("]","").split(",")
        values = [float(val) for val in Stringcodio]
        valpred = np.reshape(np.array(values), (5,136))
        prediction = None
        global graph
        with graph.as_default():
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
    app.run(host="0.0.0.0", port=int("50001"), debug=True)

