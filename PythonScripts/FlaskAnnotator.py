
#!flask/bin/python
from __future__ import print_function
from flask_cors import CORS
from flask import Flask, jsonify, abort, request, make_response, url_for
import sys
import os
import EmotionDetectorObject
from keras.models import Sequential
from keras.layers import Dense
from keras.models import model_from_json
import numpy



UPLOAD_FOLDER = './'

app = Flask(__name__, static_url_path = "")
CORS(app)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

#myemotiondetector = EmotionDetectorObject.EmotionDetectorObject()

# load json and create model
json_file = open('./models/EmoDashANN_model_v1.json', 'r')
loaded_model_json = json_file.read()
json_file.close()
loaded_model = model_from_json(loaded_model_json)
loaded_model.load_weights("./models/EmoDashANN_model_v1.h5")




    
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
    return "alice"

@app.route('/upload', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        
        if 'file' not in request.files:
            print('No file part',file=sys.stderr)
            return redirect(request.url)
        #filez = request.files['file']
        #print(filez.filename, file=sys.stderr)
        #extension = os.path.splitext(filez.filename)[1]
        #f_name = str(uuid.uuid4()) + extension
        #filez.save(os.path.join('./', f_name))
        mydata = request.files['file']
        filename = mydata.filename
        mydata.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        print(mydata, file=sys.stderr)   
        
        #the emotion detector object to be used.
        global myemotiondetector
        unsorted = myemotiondetector.classify_image(filename)
        
        print(unsorted, file=sys.stderr)
        #put the emotion detector here, the image has to be read and then analysed.
        #the client has to have a graph showing the emotions of the user
        #eye tracking also to follow the user attention?
    
        return "meh" #json.dumps({'filename':f_name})
    if request.method== 'GET':
        mydata = request.data
        #filez = request.files['file']
        print(mydata, file=sys.stderr)
        return "oh oh"

    
if __name__ == '__main__':
    app.run(debug = True)