from flask import Flask, request, url_for

import os
from keras.models import Sequential
from keras.layers import Dense
from keras.models import model_from_json
import numpy as np
import json


app = Flask(__name__)

import EmotionExtractor

em = EmotionExtractor.EmotionExtractor('baseline.npy', 'baseline_mean_sd.pickle')


@app.route('/annotate', methods=['POST'])
def upload_agent():
    if request.method == 'POST':

        data_dict = dict(request.form)
        jdata = data_dict['data']  # this is what we get in here a form with data
        myjson = jdata[0]
        mydata = json.loads(myjson)['data'][0]
        prediction = em.predict_emotion(np.array(mydata))
        body = {"messages": [
            {"Anger": round(prediction[0][0], 2), "Disgust": round(prediction[0][1], 2),
             "Fear": round(prediction[0][2], 2), "Happiness": round(prediction[0][4], 2),
             "Neutral": round(prediction[0][6], 2), "Sadness": round(prediction[0][5], 2),
             "Surprise": round(prediction[0][3], 2)}]}

        return body


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=int("50000"), debug=True)