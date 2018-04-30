import os;
import threading;
import logging;
import random;
import MicroPhoneRecorder
import datetime

from requests.exceptions import ConnectionError;
from socketIO_client_nexus import SocketIO, BaseNamespace;
from urlparse import urlparse;

logging.getLogger('socketIO-client-nexus').setLevel(logging.ERROR);
logging.getLogger('root').setLevel(logging.INFO);
logging.basicConfig();

vera_hub_address = urlparse(os.getenv('VERA_HUB_URI', 'http://localhost:3005'));
vera_rig_id = os.getenv('VERA_RIG_ID', 'TESTSPACE');
vera_type = 'vera-preprocessor';
vera_emotion_processor_address = urlparse(os.getenv('VERA_EMOTION_PROCESSOR_ADDRESS', 'http://vera.northeurope.cloudapp.azure.com:50001/annotate'));

#vera_emotion_processor_address = urlparse(os.getenv('VERA_EMOTION_PROCESSOR_ADDRESS', 'http://vera.northeurope.cloudapp.azure.com:50001/annotate'));
vera_mongo_db = urlparse(os.getenv("VERA_FEATURES_DB", "mongodb://127.0.0.1:27017/VERAPreProcessor"))
print(vera_mongo_db.geturl())
""" global variables """
vera_namespace = None;
event = None;
emotions = [];
""" microphone """
mt = MicroPhoneRecorder.MicroPhoneRecorder(RATE= 8000, Device=1, WAVE_OUTPUT_FILENAME="output", EXPORT_FOLDER="Agent", BASELINE= './mean_std.csv', URL=vera_emotion_processor_address.geturl())
""" set mongo db"""

try:
    mt.set_mongo_db(URL = vera_mongo_db.geturl())
except:
    print("WARNING: Mongo DB not set up")
    pass

def get_emotions():
    global mt
    data = mt.pop_emotions()
    return data;

def vera_preprocess(e, s, d):
    """ Replace this code with VERA pre-processor code for audio processing """
    while True:
        if not e.isSet():
            logging.info('processing...');
            data = get_emotions();
            #print("processing")
            if data!=None:
                global emotions
                callid= d.get("callid") # we should get all the relevant information here.
                callagentid = d.get("callagentid")
                #data["callid"] = callid
                #data["callagentid"] = callagentid
                #data["rigid"] = vera_rig_id
                mt.save_in_mongo_db({ 'rigid': vera_rig_id, 'type': vera_type, 'callid': callid, 'callagentid': callagentid, 'data': data })
                #print("===START READING===")
                #print(data)
                #print("Right Channel")
                #print(data['right_emotion'][0])
                #print("Left Channel")
                #print(data['left_emotion'][0])
                #print("===END READING===")
                if not e.isSet(): When alreadly stopped do not add current emotions
                    emotions.append(data['right_emotion'][0])#it will get big at a certain point
                    s.emit('emotion', { 'rigid': vera_rig_id, 'type': vera_type, 'callid': callid, 'callagentid': callagentid, 'emotions': data['right_emotion'][0] })
            


class Namespace(BaseNamespace):
    """ The binding to 'connected' event is done automatically by namespace based on name """
    def on_connected(data):
        vera_namespace.emit("join-space", { 'rigid': vera_rig_id, 'type': vera_type });


""" Events for which there is no automatic binding in the namespace. """

def on_vera_start(data):
    """ Start second thread with the VERA audio processing """
    print(data)
    global event;
    global vera_namespace;
    global mt;
    
    mt.start_recording()
    
    event = threading.Event();
    thread = threading.Thread(name='preprocessor', target=vera_preprocess, args=(event, vera_namespace,data));
    thread.start();

    """ Signal other modules in space that processing has been started """
    data['type'] = vera_type;
    vera_namespace.emit("vera-started", data);


def on_vera_stop(data):
    """ Signal 2nd thread to stop processing by setting the threading event. This will exit the thread. """
    global event
    global mt
    event.set()
    mt.stop_recording()
    print("stopped")
    """ Signal other modules in space that processing has been stopped """
    global vera_namespace
    data['type'] = vera_type
    global emotions
    data.update({ 'emotions': emotions })
    vera_namespace.emit("vera-stopped", data)
    del emotions[:]


try:
    socketIO  = SocketIO(vera_hub_address.hostname, vera_hub_address.port, Namespace);
    vera_namespace = socketIO.define(Namespace, '/VERA')
    vera_namespace.on('vera-start', on_vera_start);
    vera_namespace.on('vera-stop', on_vera_stop);
    socketIO.wait();
except ConnectionError:
    print('The server is down. Try again later.')





