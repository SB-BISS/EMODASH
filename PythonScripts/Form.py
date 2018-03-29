import Tkinter
from Tkinter import *
import tkMessageBox
import MicroPhoneRecorder


#em = EmotionExtractor.EmotionExtractor('baseline.npy', 'baseline_mean_sd.pickle')

mt = MicroPhoneRecorder.MicroPhoneRecorder(Device=1, WAVE_OUTPUT_FILENAME="output", EXPORT_FOLDER="Agent", BAELINE= 'baseline_mean_sd.pickle')
#mt2 = MicroPhoneRecorder.MicroPhoneRecorder(Device=1,  WAVE_OUTPUT_FILENAME="output2", EXPORT_FOLDER="Customer",EMOTION_EXTRACTOR= em)

root = Tk()
top = Tkinter.Frame(root, width=100, height=100, background="bisque")

#top.maxsize(800,800)



def start_recording():
    mt.start_recording()
    #mt2.start_recording()

def end_recording():
    mt.stop_recording()
    #mt2.stop_recording()

start_rec = Button(top, text ="START RECORDING", command = start_recording)

end_rec = Button(top, text ="END RECORDING", command = end_recording)


text = Text(top, height=10)
text.insert(INSERT, "customer_id")
text2 = Text(top, height=10)
text2.insert(INSERT,"customer_name")



text.pack()
text2.pack()
start_rec.pack()
end_rec.pack()
top.pack()
# Code to add widgets will go here...
root.mainloop()