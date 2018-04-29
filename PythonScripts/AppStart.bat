set VERA_EMOTION_PROCESSOR_ADDRESS=http://vera.northeurope.cloudapp.azure.com:50001/annotate
set VERA_FEATURES_DB=mongodb://127.0.0.1:27017/VERAPreProcessor
echo %VERA_EMOTION_PROCESSOR_ADDRESS%
echo %VERA_FEATURES_DB%
python app.py