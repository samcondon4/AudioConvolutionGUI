import matplotlib
matplotlib.use("TkAgg")
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import matplotlib.animation as animation
from matplotlib import style
import tkinter as tk
import numpy as np
import soundcard as sc
from scipy.io.wavfile import read



LARGE_FONT = ("Verdanna", 12)
style.use("ggplot")

f = Figure(figsize=(30,20), dpi=100)
gs = f.add_gridspec(2,5)

recordtime = 3


def ReadWav(wavstrg):
    red = read(wavstrg)
    samps = []
    for k in red[1]:
        samps.append(k[1])
    samps = samps/np.max(samps)
    return samps

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
        self.mic = sc.get_microphone('Shure')

        tk.Frame.__init__(self,parent_)
        label = tk.Label(self, text="Convolution in Audio Demo", font=LARGE_FONT)
        label.pack(pady=10,padx=10)

        record = tk.Button(self, text="Record Audio", command=lambda: self.record_button())
        record.pack()
    
    def record_button(self):
        recording = self.mic.record(samplerate=44100,numframes=recordtime*44100)
        recording = recording/np.max(recording)
        rec = []
        for k in recording:
            rec.append(k[0])
        self.controller.frames[DisplayRecording].set_recording(rec) 
        self.controller.show_frame(DisplayRecording)

class DisplayRecording(tk.Frame):

    def __init__(self, parent_, controller_):
        
        ##PAGE ATTRIBUTES###################
        self.parent = parent_
        self.controller = controller_
        
        self.recording = np.zeros(recordtime*44100)
        self.recsamps = np.arange(0,recordtime*44100,1)
        self.RECplot = f.add_subplot(gs[0,2])
        self.RECplot.title.set_text('Current Waveform')
        
        self.MLdata = ReadWav('Masonic Lodge.wav')
        self.MLsamps = np.arange(0,len(self.MLdata),1)
        self.MLplot = f.add_subplot(gs[1,0])
        self.MLplot.title.set_text('Masonic Lodge')
        self.MLplot.plot(self.MLsamps,self.MLdata)

        self.NDRdata = ReadWav('Nice Drum Room.wav')
        self.NDRsamps = np.arange(0,len(self.NDRdata),1)
        self.NDRplot = f.add_subplot(gs[1,1])
        self.NDRplot.title.set_text('Nice Drum Room')
        self.NDRplot.plot(self.NDRsamps,self.NDRdata)

        self.PGdata = ReadWav('Parking Garage.wav')
        self.PGsamps = np.arange(0,len(self.PGdata),1)
        self.PGplot = f.add_subplot(gs[1,2])
        self.PGplot.title.set_text('Parking Garage')
        self.PGplot.plot(self.PGsamps,self.PGdata)

        self.RGTdata = ReadWav('Right Glass Triangle.wav')
        self.RGTsamps = np.arange(0,len(self.RGTdata),1)
        self.RGTplot = f.add_subplot(gs[1,3])
        self.RGTplot.title.set_text('Right Glass Triangle')
        self.RGTplot.plot(self.RGTsamps,self.RGTdata)

        self.SCONVdata = np.zeros(recordtime*44100)
        self.SCONVsamps = np.arange(0,recordtime*44100)
        self.SCONVplot = f.add_subplot(gs[1,4])
        self.SCONVplot.title.set_text('Record Your Own!')

        self.speaker = sc.get_speaker('Built-in')
        ####################################

        tk.Frame.__init__(self,parent_)

        label = tk.Label(self, text="Waveform", font=LARGE_FONT)
        label.grid(row=0, column=1, padx=10, pady=10)

        ##BUTTONS###################################################################################
        homeret = tk.Button(self, text="Return to Home", command=lambda: self.ret_home())
        homeret.grid(row=2,column=0)

        playrec = tk.Button(self, text="Play Recording", command=lambda: self.play_recording())
        playrec.grid(row=3,column=2)
        ############################################################################################
        
        ##PLOTS##############################################
        

        #####################################################

        canvas = FigureCanvasTkAgg(f, self)
        canvas.draw()
        canvas.get_tk_widget().grid(row=1,column=1)

    #Pass a list or numpy array
    def set_recording(self,rec):
        self.recording = np.array(rec)

    def ret_home(self):
        self.controller.show_frame(StartPage)
    
    def play_recording(self):
        self.speaker.play(self.recording, samplerate=44100)

    def show_waveform(self,k):
        self.RECplot.clear()
        self.RECplot.plot(self.recsamps, self.recording)


###################################################################################


app = TkGui()
app.attributes('-type', 'dialog')
ani = animation.FuncAnimation(f, app.frames[DisplayRecording].show_waveform, interval = 1000)
while True:
    app.update_idletasks()
    app.update()




