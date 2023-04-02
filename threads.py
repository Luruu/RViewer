''' 
    Model
'''

import os.path
import datetime
import sys
from PySide6.QtCore import *
from PySide6.QtGui import *
from PySide6.QtWidgets import *

class WhisperModel(QThread):

    def __init__(self, controller, name_video, path_video):
            QThread.__init__(self)
            self.name_video = name_video
            self.path_video = path_video
            self.controller = controller
        
    def run(self):
        self.create_subtitles_and_set_subtitles(self.name_video, self.path_video)


    def create_subtitles_and_set_subtitles(self, name_video, path_video):
        ''' imports are here because too heavy to import at startup'''
        import whisper 
        import torch
        
        DEVICE = "cuda" if torch.cuda.is_available() else "cpu"
        NAME_MODEL = 'small'
        print("Loading Whisper {} Model on '{}' [torch.cuda {}]".format(NAME_MODEL.upper(), "GPU" if DEVICE == "cuda" else "CPU", "available" if DEVICE == "cuda" else "NOT available"))
        model = whisper.load_model(NAME_MODEL, device=DEVICE)

        print("Creating Subtitles...")
        result = model.transcribe(path_video, verbose=True, without_timestamps=False, language="en")
        
        print("Subtitles created!")

        self.create_srt(name_video, result)
        
        print("file Subtitles created!")
        srt = os.path.join('srt', "{}.srt".format(name_video)) 
  
        if self.controller.w_player.set_subtitle(srt) == 1:
            print("subtitles added correctly")
        else:
            print("error: cannot add subtitles")
        

    def create_srt(self,name_video, result):
        self.str_out = ""
        for key in result["segments"]:
            self.str_out += "{}\n{} --> {}\n{}\n\n".format(key["id"]+1, self.convert_ss_to_hmmss(key["start"]),self.convert_ss_to_hmmss(key["end"]),key["text"])
        
        with open("srt/{}.srt".format(name_video), 'w', encoding="utf-8") as f:
            f.write(self.str_out)

    def convert_ss_to_hmmss(self, ss):
        return str(datetime.timedelta(seconds=ss))

# to avoid freezes, I use this QThread as a timer
class ThreadTimer(QThread):
    update_gui = Signal()
    def __init__(self,controller):
        QThread.__init__(self)
        self.controller = controller
        
    def run(self):
        while not self.isInterruptionRequested():
            # print(self.controller.sem.available())  
            if self.controller.sem.available() == 0 and self.controller.w_player.is_paused:  
                print("lock")  
                self.controller.sem.acquire(1)
                print("unlock")  
            QThread.sleep(1)
                
            # MacOS has problem if a external thread updates UI objects
            if sys.platform == "darwin":
                self.update_gui.emit() 
            else:
                self.controller.update_gui()

            if not self.controller.w_player.is_playing(): # if is paused or stopped
                self.controller.window.btnPlayPause.setText(">")
                if not self.controller.w_player.is_paused: # if is stopped
                    self.controller.w_player.stop()
                    if self.controller.m_player.player_preferences["loop_video"]:
                        self.controller.window.btnPlayPause.setEnabled(False)
                        QThread.sleep(3)
                        self.controller.play()
                        self.controller.window.btnPlayPause.setEnabled(True)