'''
    controller
'''


from views import PlayerView

from mainview import MainView

from model import PlayerModel, VideoModel


import sys
import time
import os
from PySide6.QtCore import *
from PySide6.QtGui import *
from PySide6.QtWidgets import *

class Controller():

    def __init__(self):
        self.program_name = "RV"

        ''' source_path is for testing only '''
        source_path = ["test/test_sub.mkv", "test/test_without_subs.mp4", "test/input.mkv", "test/output.mkv", "test/B.mp3", "test/audio.mp3", "test/audio_short.wav",
                       "test/video2.mkv", "test/video.mp4", "test/sample.mp4", "test/1.mkv", "test/video_test.mp4"]
       

        sys.argv += [source_path[4]]

        if not os.path.exists(sys.argv[1]):
            print("error: video file does not exists.")
            sys.exit()

        self.sem_player = QSemaphore(0)
        self.w_player = PlayerView(self)
        self.w_player.start()
        self.sem_player.acquire(1)
        self.m_player = PlayerModel()
        self.window = MainView(self.program_name, self, self.m_player.player_preferences)
        self.window.whisper_window.combobox1.setCurrentText(self.m_player.player_preferences["whisper_language"])
        self.window.whisper_window.combobox2.setCurrentText(self.m_player.player_preferences["whisper_model"])
        self.window.setEnabled(False)
        self.anchorVLCtoWindow(self.w_player.get_istance_vlc_player(), self.window.videoframe.winId())

        
        self.sem = QSemaphore(0)
        self.play_pause()
        self.sem.acquire(1)
        self.m_video = VideoModel(self.m_player.player_preferences)
        

        self.thread = ThreadTimer(self)

        
        self.w_player.parse_media()
        self.window.show() 
        self.m_video.get_videoinfo_byvideo(self.w_player)
        self.initialize_gui()
        
    
        if sys.platform == "darwin":
            self.thread.update_gui.connect(self.update_gui)
        
        self.whisper = None
        self.window.whisper_window.name_video = self.m_video.name_video
        self.set_view_connections()
        self.thread.start()
        self.window.setEnabled(True)
    
        sys.exit(self.window.app.exec())
        
    

    def play(self):
        self.w_player.play()
        self.w_player.is_paused = False
        self.window.btnPlayPause.setText("||")
        self.window.btnPlayPause.setShortcut(self.m_player.player_preferences["playpause_shortkey"])  
        self.window.btnPlayPause.setStyleSheet('QPushButton {background-color: #981c12; color: white;}')
        if self.sem.available() == 0:
            self.sem.release(1)
                      
    def pause(self):
        if self.w_player.is_playing():
            self.w_player.pause()
            self.w_player.is_paused = True
            self.window.btnPlayPause.setText(">")
            self.window.btnPlayPause.setStyleSheet('QPushButton {background-color: green; color: white;}')
            self.window.btnPlayPause.setShortcut(self.m_player.player_preferences["playpause_shortkey"])  
      
    def play_pause(self):
        if self.w_player.is_playing():
            if self.sem.available() >= 1:
                self.sem.acquire(1)
            self.pause()
        else:
            if self.sem.available() == 0:
                self.sem.release(1)
            self.play()

    def changeSpeedVideo(self):
        # for example: value on trackbar for 1.0x is 5, so 5/5 = 1. For 2.0x is 10, so 10/5 = 2 and so on.
        new_speed = self.window.speed_slider.value() / 5
        self.window.label_speed.setText(" " + str(new_speed) + "x")
        self.w_player.set_rate(new_speed)


    def __check_track_video_preference(self):
        # use video speed instead player speed
        if self.m_player.player_preferences["track_video"]:
            self.window.speed_slider.setValue(self.m_video.video_preferences["track_value"]) 
        else:
            self.window.speed_slider.setValue(self.m_player.player_preferences["track_value"]) 
        self.changeSpeedVideo()
    
    def __check_pick_up_where_you_left_off_preference(self):
        # if pick up where you left off is true, load last position
        if self.m_player.player_preferences["pick_up_where_you_left_off"]:
            self.w_player.set_time(self.m_video.video_preferences["load_pos"])

    
    def __check_volume_preference(self):
        # self.w_player.set_volume(self.m_video.video_preferences["volume_value"])
        self.window.volume_slider.setValue(self.m_video.video_preferences["volume_value"])
    
    def __check_if_audiotrack_exist(self):
        if self.w_player.get_audio_count() <= 0:
            self.window.btnSubtitle.setEnabled(False)
            self.window.btnSubtitle.setText("no audio track found")
            return False
        else:
            return True

    def __check_show_subtitle_if_available_preference(self):
        
        #check if video contains audiotracks
        if not self.__check_if_audiotrack_exist():
            return
        
        # if user want show subtitles
        if self.m_player.player_preferences["show_subtitle_if_available"]:
            str_path = os.path.join('srt', "{}.srt".format(self.m_video.name_video)) 

        # if file contains subtitles
            if self.w_player.get_sub_count() >= 2: # note: 1 is -1 for no subtitles
                self.show_subtitles()
            # if file does not contain subtitles but srt file exists 
            elif os.path.exists(str_path):
                self.w_player.set_subtitle(str_path)
                self.buttonsub_operation = 0
                self.window.btnSubtitle.setText("hide subtitles")
            else:
                print("no sutbtitles found")

                self.buttonsub_operation = 2

        else:
            self.buttonsub_operation = 2
            self.window.btnSubtitle.setText("add subtitles")
        

    def initialize_gui(self): 
        self.m_video.load_videopreferences()

        self.__check_track_video_preference()
        
        self.__check_pick_up_where_you_left_off_preference()
        
        self.__check_volume_preference()
        
        self.__check_show_subtitle_if_available_preference()
       
        

    def hide_subtitles(self):
        self.buttonsub_operation = 1
        self.window.btnSubtitle.setText("show subtitles")
        self.w_player.set_sub(self.w_player.get_sub_descriptions()[0][0])

    def show_subtitles(self):
        self.buttonsub_operation = 0
        self.window.btnSubtitle.setText("hide subtitles")
        self.w_player.set_sub(self.w_player.get_sub_descriptions()[1][0])

    def handle_subtitles(self):
        if self.buttonsub_operation == 0: # hide subtitles
            self.hide_subtitles()
        elif self.buttonsub_operation == 1: # show subtitles
            self.show_subtitles()
        elif self.buttonsub_operation == 2:   # whisper
            self.window.show_whisper_window()
        else:
            print("else handle_subtitle error!!")

    def handle_stderr(self):
        data = self.whisper.readAllStandardError()
        stderr = bytes(data).decode("utf8")
        # Extract progress if it is in the data.
        self.window.whisper_window.textedit.append(stderr)

    def handle_stdout(self):
        data = self.whisper.readAllStandardOutput()
        stdout = bytes(data).decode("utf8")
        self.window.whisper_window.textedit.append(stdout)

    def handle_state(self, state):
        states = {
            QProcess.NotRunning: 'Not running',
            QProcess.Starting: 'Starting',
            QProcess.Running: 'Running',
        }
        state_name = states[state]
        self.window.whisper_window.textedit.append(f"State changed: {state_name}")

    def process_finished(self):
        self.window.whisper_window.setEnabled(True)
        self.window.setEnabled(True)
        
        srt_file_name = os.path.join('srt', "{}.srt".format(self.m_video.name_video))
        # if process is completed, it will have created the srt file.
        if os.path.exists(srt_file_name): 
            self.window.whisper_window.textedit.append("Process completed! :)")
            if self.set_subtitles_by_file(srt_file_name):
                self.window.whisper_window.textedit.append("{}: srt file Subtitles have been set up correctly!".format(time.strftime("%H:%M:%S", time.localtime()))) 
            else:
                self.window.whisper_window.textedit.append("{}: error! cannot create srt file Subtitles.".format(time.strftime("%H:%M:%S", time.localtime())))
        else: # if process is interrupted, it will not have created the srt file.
            self.window.whisper_window.textedit.append("Process interrupted! :(")

        self.whisper = None


    def do_subtitles(self):
        self.pause() # pause video 
        if self.whisper is None:
            self.window.whisper_window.setEnabled(False)
            self.window.setEnabled(False)
            self.whisper = QProcess()
            self.whisper.readyReadStandardOutput.connect(self.handle_stdout)
            self.whisper.readyReadStandardError.connect(self.handle_stderr)
            self.whisper.stateChanged.connect(self.handle_state)
            self.whisper.finished.connect(self.process_finished)
            
    
        # os.environ['VIRTUAL_ENV']
        if sys.platform == "win32":
            python = os.path.join("env", "Scripts", "python.exe")
        else:
            python = os.path.join("env", "bin", "python")
         
        
    
        self.whisper.start(python, ["subtitle.py", self.m_video.name_video, sys.argv[1], self.window.whisper_window.get_language_selected(),self.window.whisper_window.combobox2.currentText()])
            

            

    def whisper_view_close(self):
        if self.whisper is not None:
            self.whisper.close()

        self.window.setEnabled(True)

        if self.w_player.get_sub_count() > 0:
            self.buttonsub_operation = 0
            self.window.btnSubtitle.setText("hide subtitles")
    


    def set_subtitles_by_file(self, srt):
        return self.w_player.set_subtitle(srt) == 1

    def update_gui(self):
        if self.m_video.video_info["Artist"] is None:
            new_title = "{} - {} [{}]".format(self.program_name, self.m_video.video_info['Title'], self.m_video.video_info["Duration_hh_mm_ss"])
        else:
            new_title = "{} - {} by {} [{}]".format(self.program_name, self.m_video.video_info['Title'], self.m_video.video_info["Artist"], self.m_video.video_info["Duration_hh_mm_ss"])
        
        self.window.setWindowTitle(new_title)
        self.window.loadbar.setMaximum(self.m_video.video_info["Duration"])
        self.m_video.video_info["Position"] = self.w_player.get_time()
        self.window.loadbar.setValue(int(self.m_video.video_info["Position"]))
        self.window.labelposition.setText(self.m_video.convert_ms_to_hmmss(self.m_video.video_info["Position"]))
        self.window.labelduration.setText(self.m_video.convert_ms_to_hmmss(self.m_video.video_info["Duration"] - self.m_video.video_info["Position"]))


    ''' This slot is only used to handle mouse clicks.'''
    def slider_clicked(self):
        if self.window.loadbar.mouse_pressed:
            self.window.loadbar.mouse_pressed = False
            self.pause()
            self.w_player.set_time(self.window.loadbar.value())
            self.update_gui()
            self.play()
            
    def goback_and_update_gui(self):
        self.w_player.go_back(self.m_video.convert_seconds_to_ms(self.m_player.player_preferences["back_value"])) 
        self.update_gui()

    def goforward_and_update_gui(self):
        self.w_player.go_forward(self.m_video.convert_seconds_to_ms(self.m_player.player_preferences["forward_value"])) 
        self.update_gui()
    
    def slider_released_behavior(self):
        self.w_player.set_time(self.window.loadbar.value())
        time.sleep(0.2)
        self.play()

    def set_view_connections(self):
        self.window.btnBack.clicked.connect(self.goback_and_update_gui)
        self.window.btnPlayPause.clicked.connect(self.play_pause)
        self.window.btnForward.clicked.connect(self.goforward_and_update_gui)
        self.window.btnpreferences.clicked.connect(self.window.show_preference_window)
        self.window.btnSubtitle.clicked.connect(self.handle_subtitles)
        self.window.speed_slider.valueChanged.connect(self.changeSpeedVideo)

        self.window.loadbar.sliderPressed.connect(self.pause)
        self.window.loadbar.sliderReleased.connect(self.slider_released_behavior)
        self.window.loadbar.valueChanged.connect(self.slider_clicked)
        self.window.volume_slider.valueChanged.connect(lambda: self.w_player.set_volume(self.window.volume_slider.value()))

        self.window.tool_bar2.orientationChanged.connect(self.window.set_loadbar2orientation)

        self.window.whisper_window.createbutton.clicked.connect(self.do_subtitles)

    def anchorVLCtoWindow(self, player, id):
        if sys.platform.startswith('linux'): # for Linux using the X Server
            player.set_xwindow(id)
        elif sys.platform == "win32": # for Windows
            player.set_hwnd(id)
        elif sys.platform == "darwin": # for MacOS
            player.set_nsobject(id)
        else:
            print("ERROR: this software does not work with", sys.platform)
            sys.exit()
    
    def close_program(self, event, track_pos,load_pos):
        print("closing..")
        self.window.preference_window.close()
        self.window.whisper_window.close()
        self.thread.terminate()
        
        self.m_video.save_video_preferences(track_pos=track_pos, load_pos=load_pos, vol= self.w_player.get_volume())
        geometry = self.window.geometry()
        self.m_player.save_player_preferences(x=geometry.x(), y=geometry.y(), dim=geometry.width(), hei=geometry.height(), whisper_len=self.window.whisper_window.combobox1.currentText(), whisper_model=self.window.whisper_window.combobox2.currentText())
        


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
    
                            
            
if __name__ == '__main__':
    c = Controller()