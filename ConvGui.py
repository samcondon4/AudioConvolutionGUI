import tkinter as tk
import numpy as np
import soundcard as sc
import thinkdsp



LARGE_FONT = ("Verdanna", 12)




###################TKINTER GUI BASELINE###########################
class TkGui(tk.Tk):

    def __init__(self, *args, **kwargs):
        
        tk.Tk.__init__(self, *args, **kwargs)
        
        ##dictionary to hold all frames for application##
        self.frames = {}

        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)
        
        for F in [StartPage, DisplayRecording]:
            frame = F(container, self)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(StartPage)

    def show_frame(self, cont):

        frame = self.frames[cont]
        frame.tkraise() 

    def add_frame(self, frame, framename="StartPage"):

       self.frames[framename] = frame 

#####################################################################

######DEFINE PAGES OF GUI##################################################
class StartPage(tk.Frame):

    def __init__(self, parent_, controller_):
        
        self.parent = parent_
        self.controller = controller_
        
        tk.Frame.__init__(self,parent_)
        label = tk.Label(self, text="Convolution in Audio Demo", font=LARGE_FONT)
        label.pack(pady=10,padx=10)

        record = tk.Button(self, text="Record Audio", command=lambda: self.record_button())
        record.pack()
    
    def record_button(self):
        mic = sc.get_microphone('Shure')
        recording = mic.record(samplerate=44100,numframes=2*44100)
        recording = recording/np.max(recording)
        rec = []
        for k in recording:
            rec.append(k[0])
        self.controller.frames[DisplayRecording].set_recording(rec) 
        self.controller.show_frame(DisplayRecording)
        


class DisplayRecording(tk.Frame):

    def __init__(self, parent_, controller_):
        
        self.parent = parent_
        self.controller = controller_

        self.recording = []
        
        tk.Frame.__init__(self,parent_)

        label = tk.Label(self, text="Waveform", font=LARGE_FONT)
        label.pack(pady=10,padx=10)

        homeret = tk.Button(self, text="Return to Home", command=lambda: self.ret_home())
        homeret.pack()

        playrec = tk.Button(self, text="Play Recording", command=lambda: self.play_recording())
        playrec.pack()
 
    #Pass a list or numpy array
    def set_recording(self,rec):
        self.recording = np.array(rec)

    def ret_home(self):
        self.controller.show_frame(StartPage)
    
    def play_recording(self):
        defaultspeaker = sc.default_speaker()
        defaultspeaker.play(self.recording, samplerate=44100)

###################################################################################


app = TkGui()
app.attributes('-type', 'dialog')
while True:
    app.update_idletasks()
    app.update()




