
#!flask/bin/python
from __future__ import print_function
from flask_cors import CORS
from flask import Flask, jsonify, abort, request, make_response, url_for
import sys
import os
from keras.models import Sequential
from keras.layers import Dense
from keras.models import model_from_json
import numpy
import FeatureExtractor
import json

UPLOAD_FOLDER = './'

app = Flask(__name__, static_url_path = "")
CORS(app)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

#myemotiondetector = EmotionDetectorObject.EmotionDetectorObject()

# load json and create model

model = FeatureExtractor.baseline_model()
model.load_weights('./EmoDashAnnotation/Resources/EmoDashANN_weights_v1.h5')

    
@app.errorhandler(400)
def not_found(error):
    print(error, file=sys.stderr)
    return make_response(jsonify( { 'error': 'Bad request' } ), 400)

@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify( { 'error': 'Not found' } ), 404)

@app.route('/alive', methods= ['GET'])
def alive():
    print('Hello world!', file=sys.stderr)
    return "ALIVE"

@app.route('/upload', methods=['POST'])
def upload():
    if request.method == 'POST':
        
        #filez = request.files['file']
        #print(filez.filename, file=sys.stderr)
        #extension = os.path.splitext(filez.filename)[1]
        #f_name = str(uuid.uuid4()) + extension
        #filez.save(os.path.join('./', f_name))
        #print(request.data)
        #print(request.form)
        #print(request.args)
        
        data_dict = dict(request.form)
        print(data_dict.keys())
        
        #terrible!
        jdata = data_dict['data'] #this is what we get in here a form with data
        myjson = jdata[0]
        print(type(myjson))
        mydata = json.loads(myjson)['data'][0] 
        print(mydata[0])
        
        #save the data...
        outputfilename = "./temp.wav"
        with open(outputfilename, 'wb') as output:
            output.write(bytearray(map(lambda x: chr(x % 256), mydata)))
        
        #the emotion detector object to be used.
        global model
        file_features = FeatureExtractor.extract_features(outputfilename)
        
        prediction= model.predict(file_features)
        
        #an array of probabilities...
        return json.dumps({'predictions':prediction.tolist()})
    
    
if __name__ == '__main__':
    app.run(host="0.0.0.0", port=int("50000"), debug=True)