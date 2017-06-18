
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
import urllib3
import certifi



UPLOAD_FOLDER = './'

app = Flask(__name__, static_url_path = "")
CORS(app)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

#myemotiondetector = EmotionDetectorObject.EmotionDetectorObject()

# load json and create model

model = FeatureExtractor.baseline_model()
model.load_weights('./EmoDashAnnotation/Resources/EmoDashANN_weights_v1.h5')


# use with or without proxy
http = urllib3.PoolManager(
    cert_reqs='CERT_REQUIRED', # Force certificate check.
    ca_certs=certifi.where(),  # Path to the Certifi bundle.
)
# http = urllib3.proxy_from_url('http://proxy_host:proxy_port')

# interaction for a specific Device instance - replace 'd000-e000-v000-i000-c000-e001' with your specific Device ID
url = 'https://iotmmsp1941838965trial.hanatrial.ondemand.com/com.sap.iotservices.mms/v1/api/http/data/7d9da3fb-ffcd-46cb-bb2f-cdb1c8c78c9f'

headers = urllib3.util.make_headers()

# use with authentication
# please insert correct OAuth token
headers['Authorization'] = 'Bearer bf7d76bf122dfa78f2b1e5b1899746e'
headers['Content-Type'] = 'application/json;charset=utf-8'


    
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

@app.route('/upload/customer', methods=['POST'])
def upload_customer():
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
        #print(data_dict.keys())
        
        #terrible!
        jdata = data_dict['data'] #this is what we get in here a form with data
        myjson = jdata[0]
        #print(type(myjson))
        mydata = json.loads(myjson)['data'][0] 
        #print(mydata[0])
        
        #save the data...
        outputfilename = "./temp_customer.wav"
        with open(outputfilename, 'wb') as output:
            output.write(bytearray(map(lambda x: chr(x % 256), mydata)))
        
        #the emotion detector object to be used.
        global model
        file_features = FeatureExtractor.extract_features(outputfilename)
        
        prediction= model.predict(file_features)
        
        body='{"mode":"sync", "messageType":"46e86c250974adcc08f2", "messages":[{"Anger":prediction[0], "Disgust":prediction[1], "Fear":prediction[2], "Hapiness":prediction[3],"Neutral":prediction[4],  "Sadness":prediction[5], "Surprise":prediction[6] }]}'
        
        try:
            r = http.urlopen('POST', url, body=body, headers=headers)
            print(r.status)
            print(r.data)
        
        except urllib3.exceptions.SSLError as e:
            print (e)
       
        
    
        print(prediction)
        #an array of probabilities...
        return json.dumps({'predictions': prediction.tolist()[0]})


@app.route('/upload/agent', methods=['POST'])
def upload_agent():
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
        #print(data_dict.keys())
        
        #terrible!
        jdata = data_dict['data'] #this is what we get in here a form with data
        myjson = jdata[0]
        #print(type(myjson))
        mydata = json.loads(myjson)['data'][0] 
        #print(mydata[0])
        
        #save the data...
        outputfilename = "./temp_agent.wav"
        with open(outputfilename, 'wb') as output:
            output.write(bytearray(map(lambda x: chr(x % 256), mydata)))
        
        #the emotion detector object to be used.
        global model
        file_features = FeatureExtractor.extract_features(outputfilename)
        
        prediction= model.predict(file_features)
        #TYPO IN HAPPINESS !!!
        body='{"mode":"sync", "messageType":"70281a5b78eba98c2e2c", "messages":[{"Anger":prediction[0], "Disgust":prediction[1], "Fear":prediction[2], "Hapiness":prediction[3],"Neutral":prediction[4],  "Sadness":prediction[5], "Surprise":prediction[6] }]}'
        
        try:
            r = http.urlopen('POST', url, body=body, headers=headers)
            print(r.status)
            print(r.data)
        
        except urllib3.exceptions.SSLError as e:
            print (e)
        
        print(prediction)
        #an array of probabilities...
        return json.dumps({'predictions': prediction.tolist()[0]})

    
if __name__ == '__main__':
    app.run(host="0.0.0.0", port=int("50000"), debug=True)