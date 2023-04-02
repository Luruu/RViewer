''' 
    Model
'''
import time
import os.path
import datetime
import sys
from PySide6.QtCore import *
from PySide6.QtGui import *
from PySide6.QtWidgets import *

class Whisper(QThread):
    progress_update = Signal(str, int)
    def __init__(self, controller, name_video , path_video):
            
            QThread.__init__(self)
            self.name_video = name_video
            self.path_video = path_video
            self.controller = controller
            self.lang_sub = ""
            self.model = ""
            
    def run(self):
        ''' imports are here because too heavy to import at startup'''
        self.progress_update.emit("starting Whisper..", 0) 
        import whisper 
        import torch
        
        DEVICE = "cuda" if torch.cuda.is_available() else "cpu"

        current_time = time.strftime("%H:%M:%S", time.localtime())
        
        self.progress_update.emit("{}: Loading Whisper {} Model on\n '{}' [torch.cuda {}]".format(current_time, self.model.upper(), "GPU" if DEVICE == "cuda" else "CPU", "available" if DEVICE == "cuda" else "NOT available"),1) 
        model = whisper.load_model(self.model, device=DEVICE)

        self.progress_update.emit("Creating Subtitles...", 3) 
    

        result = model.transcribe(self.path_video, verbose=False, without_timestamps=False, language=self.lang_dub)
        
        self.progress_update.emit("Subtitles created!", 4) 

        srt_file_name = os.path.join('srt', "{}.srt".format(self.name_video))
       
        self.create_srt(srt_file_name, result)
        self.progress_update.emit("srt file Subtitles created!", 5) 
        
        
        if self.controller.set_subtitles_by_file(srt_file_name):
            self.progress_update.emit("srt file Subtitles created!", 6) 
        else:
            self.progress_update.emit("error: cannot create srt file Subtitles.", 7)

    def create_srt(self,srt_file_name, result):
        self.str_out = ""
        for key in result["segments"]:
            self.str_out += "{}\n{} --> {}\n{}\n\n".format(key["id"]+1, self.convert_ss_to_hmmss(key["start"]),self.convert_ss_to_hmmss(key["end"]),key["text"])
        
        with open(srt_file_name, 'w', encoding="utf-8") as f:
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
                # print("lock")  
                self.controller.sem.acquire(1)
                # print("unlock")  
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