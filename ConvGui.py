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



LARGE_FONT = ("Verdanna", 30)
style.use("ggplot")

f = Figure(figsize=(40,15), dpi=100)
gs = f.add_gridspec(2,5)

recordtime = 3


mic = sc.get_microphone('Shure')


def ReadWav(wavstrg):
    red = read(wavstrg)
    samps = []
    for k in red[1]:
        samps.append(k[1])
    samps = samps/np.max(samps)
    return samps

def MicRecord(mic):
    recording = mic.record(samplerate=44100, numframes=recordtime*44100)
    recording = recording/np.max(recording)
    rec = []
    for k in recording:
        rec.append(k[0])
    return rec

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

        record = tk.Button(self, text="Record Audio", height=100, width=300, activebackground = 'magenta', command=lambda: self.record_button())
        record.pack()
    
    def record_button(self):
        rec = MicRecord(mic)
        self.controller.frames[DisplayRecording].set_recording(rec) 
        self.controller.show_frame(DisplayRecording)

class DisplayRecording(tk.Frame):

    def __init__(self, parent_, controller_):
        
        ##PAGE ATTRIBUTES###################
        self.parent = parent_
        self.controller = controller_
        
        self.samplist = []
        self.entry = tk.StringVar()
        
        ##tuple to store current signal to be played or to convolute##
        self.cursignal = ()

        self.recording = np.zeros(recordtime*44100)
        self.recsamps = np.arange(0,recordtime*44100,1)
        self.samplist.append((self.recsamps,self.recording))
        self.RECplot = f.add_subplot(gs[0,1])
        self.RECplot.title.set_text('(0) Current Waveform')
        self.RECplot.plot(self.recsamps,self.recording)

        self.conv = []
        self.convsamps = []
        self.samplist.append((self.convsamps, self.conv))
        self.CONVplot = f.add_subplot(gs[0,2])
        self.CONVplot.title.set_text('(1) Convolution Result')
        self.CONVplot.plot(self.convsamps,self.conv)

        self.MLdata = ReadWav('Masonic Lodge.wav')
        self.MLsamps = np.arange(0,len(self.MLdata),1)
        self.samplist.append((self.MLsamps,self.MLdata))
        self.MLplot = f.add_subplot(gs[1,0])
        self.MLplot.title.set_text('(2) Masonic Lodge')
        self.MLplot.plot(self.MLsamps,self.MLdata)

        self.NDRdata = ReadWav('Nice Drum Room.wav')
        self.NDRsamps = np.arange(0,len(self.NDRdata),1)
        self.samplist.append((self.NDRsamps,self.NDRdata))
        self.NDRplot = f.add_subplot(gs[1,1])
        self.NDRplot.title.set_text('(3) Nice Drum Room')
        self.NDRplot.plot(self.NDRsamps,self.NDRdata)

        self.PGdata = ReadWav('Parking Garage.wav')
        self.PGsamps = np.arange(0,len(self.PGdata),1)
        self.samplist.append((self.PGsamps,self.PGdata))
        self.PGplot = f.add_subplot(gs[1,2])
        self.PGplot.title.set_text('(4) Parking Garage')
        self.PGplot.plot(self.PGsamps,self.PGdata)

        self.RGTdata = ReadWav('Right Glass Triangle.wav')
        self.RGTsamps = np.arange(0,len(self.RGTdata),1)
        self.samplist.append((self.RGTsamps,self.RGTdata))
        self.RGTplot = f.add_subplot(gs[1,3])
        self.RGTplot.title.set_text('(5) Right Glass Triangle')
        self.RGTplot.plot(self.RGTsamps,self.RGTdata)

        self.SCONVdata = np.zeros(recordtime*44100)
        self.SCONVsamps = np.arange(0,recordtime*44100)
        self.samplist.append((self.SCONVsamps,self.SCONVdata))
        self.SCONVplot = f.add_subplot(gs[1,4])
        self.SCONVplot.title.set_text('6) Record Your Own!')

        self.speaker = sc.get_speaker('Built-in')
        ####################################

        tk.Frame.__init__(self,parent_)

        ##BUTTONS###################################################################################
        homeret = tk.Button(self, text="Return to Home", activebackground='blue',height=10, command=lambda: self.ret_home())
        homeret.pack()
        
        entry = tk.Entry(self, textvariable=self.entry) 
        entry.pack(side="left")

        playrec = tk.Button(self, text="Play Recording", activebackground='yellow', height=10, command=lambda: self.play_recording())
        playrec.pack(side="left")

        convbut = tk.Button(self, text="Convolve Signals", activebackground = 'firebrick1', height = 10, command=lambda: self.convolve())
        convbut.pack(side="right")

        convrec = tk.Button(self, text="Record Venue Impulse", activebackground='red', height=10, command=lambda: self.record_venue())
        convrec.pack(side="bottom")
        ############################################################################################
        
        ##PLOTS##############################################
                
        
        #####################################################

        canvas = FigureCanvasTkAgg(f, self)
        canvas.draw()
        canvas.get_tk_widget().pack()

    def set_recording(self,rec):
        self.recording = np.array(rec)
        self.samplist[0] = (self.recsamps,self.recording)

    def set_cursignal(self):
        inpt = self.entry.get()
        
        if(inpt.isdigit() and int(inpt)>=0 and int(inpt)<=6):
            self.cursignal = self.samplist[int(inpt)]
        else:
            self.cursignal = self.samplist[0]

    def ret_home(self):
        self.controller.show_frame(StartPage)
    
    def play_recording(self):
        self.set_cursignal()
        self.speaker.play(self.cursignal[1], samplerate=44100)

    def show_waveform(self,k):
        self.RECplot.clear()
        self.RECplot.title.set_text('(0) Current Waveform')
        self.RECplot.plot(self.recsamps, self.recording)

    def record_venue(self):
        rec = MicRecord(mic)
        self.SCONVdata = rec
        self.samplist[6] = (self.SCONVsamps, self.SCONVdata)
        self.SCONVplot.clear()
        self.SCONVplot.title.set_text('(6) Record Your Own!')
        self.SCONVplot.plot(self.SCONVsamps, self.SCONVdata)

    def convolve(self):
        self.set_cursignal()
        cursig = self.cursignal
        rec = self.recording
        samps = self.recsamps
        
        '''
        curlen = len(cursig[0])
        reclen = len(samps)
        sampdiff = curlen - reclen
       '''
        conv = np.convolve(rec, cursig[1])
        conv = conv/np.max(conv)
        convsamps = np.arange(0, len(conv), 1)

        self.conv = conv
        self.convsamps = convsamps
        self.samplist[1] = (convsamps, conv)
        self.CONVplot.clear()
        self.CONVplot.title.set_text('(1) Convolution Result')
        self.CONVplot.plot(convsamps, conv)
        
        '''
        if(sampdiff > 0):
            for k in range(sampdiff):
                np.append(rec, 0)
        elif(sampdiff < 0):
            for k in range(abs(sampdiff)):
                np.append(cursig[1], 0)
        else:
            #do nothing since the sizes of signals to be convoluted are the same
        '''

###################################################################################


app = TkGui()
app.attributes('-type', 'dialog')
ani = animation.FuncAnimation(f, app.frames[DisplayRecording].show_waveform, interval = 1000)
while True:
    app.update_idletasks()
    app.update()




