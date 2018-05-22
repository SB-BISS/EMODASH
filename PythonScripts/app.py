import os
import threading
import logging
import random
import MicroPhoneRecorder
import datetime

from requests.exceptions import ConnectionError
from socketIO_client_nexus import SocketIO, BaseNamespace
from urlparse import urlparse

from pymongo import MongoClient

logging.getLogger('socketIO-client-nexus').setLevel(logging.ERROR)
logging.getLogger('root').setLevel(logging.INFO)
logging.basicConfig()

vera_hub_address = urlparse(os.getenv('VERA_HUB_URI', 'http://localhost:3005'))
vera_rig_id = os.getenv('VERA_RIG_ID', 'TESTSPACE')
vera_type = 'vera-preprocessor'
vera_emotion_processor_address = urlparse(os.getenv('VERA_EMOTION_PROCESSOR_ADDRESS', 'http://vera.northeurope.cloudapp.azure.com:50001/annotate'))
vera_mongo_db = urlparse(os.getenv("VERA_FEATURES_DB", "mongodb://127.0.0.1:27017/VERAPreProcessor"))


""" global variables """
mongo_features_collection = None
callinfo = { 'callid': None, 'callagentid': None }
vera_namespace = None
microphone = MicroPhoneRecorder.MicroPhoneRecorder(RATE= 8000, Device=1, WAVE_OUTPUT_FILENAME="output", EXPORT_FOLDER="Agent", BASELINE= './mean_std.csv', URL=vera_emotion_processor_address.geturl())

""" Set eventhandler for MicroPhoneRecorder events """

def onEmotionsChanged(self, data):
    global callinfo
    vera_namespace.emit('emotion', { 'rigid': vera_rig_id, 'type': vera_type, 'callid': callinfo['callid'], 'callagentid': callinfo['callagentid'], 'duration': data['duration'], 'emotions': data['right_emotion'][0] })
    save_in_mongo_db(self, { 'rigid': vera_rig_id, 'type': vera_type, 'callid': callinfo['callid'], 'callagentid': callinfo['callagentid'], 'data': data })

microphone.on('emotionsChanged', onEmotionsChanged)


""" Event handlers for hub events. """

def on_vera_start(data):
    """ Start second thread with the VERA audio processing """
    print(data)
    global callinfo 
    callinfo['callid'] = data['callid']
    callinfo['callagentid'] = data['callagentid']

    global microphone
    microphone.start_recording()
    
    """ Signal other modules in space that processing has been started """
    data['type'] = vera_type
    global vera_namespace
    vera_namespace.emit("vera-started", data)

def on_vera_stop(data):
    global microphone
    microphone.stop_recording()
    print("stopped")

    """ Signal other modules in space that processing has been stopped """
    global vera_namespace
    data['type'] = vera_type
    vera_namespace.emit("vera-stopped", data)

    global callinfo
    callinfo['callid'] = None
    callinfo['callagentid'] = None

class Namespace(BaseNamespace):
    """ The binding to 'connected' event is done automatically by namespace based on name """
    def on_connected(self):
        vera_namespace.emit("join-space", { 'rigid': vera_rig_id, 'type': vera_type })


""" Setup MongoDB """
def save_in_mongo_db(self, data):
    global mongo_features_collection
    if mongo_features_collection is None:
        try:
            mongo_features_collection = MongoClient(vera_mongo_db.geturl()).VERAPreProcessor.features
        except:
            print("WARNING: Mongo DB not set up")
            pass

    if (not mongo_features_collection is None):
        try:
            data['createdAt'] = datetime.datetime.now()
            data['calldatetime'] = datetime.datetime.now()
            mongo_features_collection.insert(data, w=0)
        except:
            print("NOT SAVED, EXCEPTION DURING SAVING in MONGODB")
            pass

""" Setup Socket.io client and start listening for events """
try:
    socketIO  = SocketIO(host=vera_hub_address.hostname, port=vera_hub_address.port, Namespace=Namespace, wait_for_connection=True)
    vera_namespace = socketIO.define(Namespace, '/VERA')
    vera_namespace.on('vera-start', on_vera_start)
    vera_namespace.on('vera-stop', on_vera_stop)
    print('Connected to VERA Hub.')
    socketIO.wait()
except ConnectionError:
    print('The server is down. Try again later.')
