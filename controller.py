'''
    controller
'''

from view import PlayerView, WindowView
from model import PlayerModel, VideoModel
import sys
import time
from PySide6.QtCore import *
from PySide6.QtGui import *
from PySide6.QtWidgets import *

class Controller():

    def __init__(self):
        self.program_name = "RV"
        # source_path is for testing only
        source_path = "test/test_sub.mkv"
        #source_path = "test/input.mkv"
        # source_path = "test/B.mp3"

        sys.argv += [source_path]

        
        self.w_player = PlayerView()
        self.m_player = PlayerModel()
        self.window = WindowView(self.program_name, self, self.m_player.player_preferences)
        self.anchorVLCtoWindow(self.w_player.get_istance_vlc_player(), self.window.videoframe.winId())
        
        
        self.sem = QSemaphore(1)
        self.play_pause()
        self.m_video = VideoModel(self.m_player.player_preferences)
        

        self.set_view_connections()
        self.w_player.parse_media()
        self.window.show() 
        self.m_video.get_videoinfo_byvideo(self.w_player)
        self.initialize_gui()
        
        
        self.thread = self.ThreadTimer(self)
        self.thread.update_gui.connect(self.update_gui)
        self.thread.start()
        
        sys.exit(self.window.app.exec())
    

    def play(self):
        self.w_player.play()
        self.w_player.is_paused = False
        self.window.btnPlayPause.setText("||")
        self.window.btnPlayPause.setStyleSheet('QPushButton {background-color: #981c12; color: white;}')
        if self.sem.available() == 0:
            self.sem.release(2)
            
        
    def pause(self):
        self.w_player.pause()
        self.w_player.is_paused = True
        self.window.btnPlayPause.setText(">")
        self.window.btnPlayPause.setStyleSheet('QPushButton {background-color: green; color: white;}')
        self.sem.acquire(1)

    def play_pause(self):
        self.pause() if self.w_player.is_playing() else self.play()

    def changeSpeedVideo(self):
        # for example: value on trackbar for 1.0x is 5, so 5/5 = 1. For 2.0x is 10, so 10/5 = 2 and so on.
        new_speed = self.window.speed_slider.value() / 5
        self.window.label_speed.setText(" " + str(new_speed) + "x")
        self.w_player.set_rate(new_speed)


    def initialize_gui(self): 
        self.m_video.load_videopreferences()
        self.window.speed_slider.setValue(self.m_video.video_preferences["track_value"])  
        self.changeSpeedVideo()
        self.w_player.set_time(self.m_video.video_preferences["load_pos"])

    def update_gui(self):
        new_title = "{} - {} [{}]".format(self.program_name, self.m_video.video_info['Title'], self.m_video.video_info["Duration_hh_mm_ss"])
        self.window.setWindowTitle(new_title)
        self.window.loadbar.setMaximum(self.m_video.video_info["Duration"])
        self.m_video.video_info["Position"] = self.w_player.get_time()
        self.window.loadbar.setValue(int(self.m_video.video_info["Position"]))
        self.window.labelposition.setText(self.m_video.convert_ms_to_hmmss(self.m_video.video_info["Position"]))
        self.window.labelduration.setText(self.m_video.convert_ms_to_hmmss(self.m_video.video_info["Duration"] - self.m_video.video_info["Position"]))


    ''' This slot is only just used to handle mouse clicks.'''
    def slider_clicked(self):
        if self.window.loadbar.mouse_pressed:
            self.window.loadbar.mouse_pressed = False
            self.w_player.set_time(self.window.loadbar.value())
            self.update_gui()
            
    def goback_and_update_gui(self):
        self.w_player.go_back(self.m_video.convert_seconds_to_ms(self.m_player.player_preferences["back_value"])) 
        self.update_gui()

    def goforward_and_update_gui(self):
        self.w_player.go_forward(self.m_video.convert_seconds_to_ms(self.m_player.player_preferences["forward_value"])) 
        self.update_gui()
    


    def set_view_connections(self):
        self.window.btnBack.clicked.connect(self.goback_and_update_gui)
        self.window.btnPlayPause.clicked.connect(self.play_pause)
        self.window.btnForward.clicked.connect(self.goforward_and_update_gui)
        self.window.btnpreferences.clicked.connect(self.window.show_preference_window)

        self.window.speed_slider.valueChanged.connect(self.changeSpeedVideo)

        self.window.loadbar.sliderMoved.connect(lambda: self.w_player.set_time(self.window.loadbar.value()))
        self.window.loadbar.sliderPressed.connect(self.pause)
        self.window.loadbar.sliderReleased.connect(self.play)
        self.window.loadbar.valueChanged.connect(self.slider_clicked)
        self.window.tool_bar2.orientationChanged.connect(self.window.set_loadbar2orientation)

    def anchorVLCtoWindow(self, player, id):
        if sys.platform.startswith('linux'): # for Linux using the X Server
            player.set_xwindow(id)
        elif sys.platform == "win32": # for Windows
            player.set_hwnd(id)
        elif sys.platform == "darwin": # for MacOS
            player.set_nsobject(id)
        else:
            print("ERROR: this software does not work with", sys.platform)
            exit()
    
    def close_program(self, event, track_pos,load_pos):
        self.thread.terminate()
        self.m_video.save_video_preferences(track_pos=track_pos, load_pos=load_pos, vol= self.w_player.get_volume())
        geometry = self.window.geometry()
        self.m_player.save_player_preferences(x=geometry.x(), y=geometry.y(), dim=geometry.width(), hei=geometry.height())


    # to avoid freezes, I use this QThread as a timer
    class ThreadTimer(QThread):
        update_gui = Signal()
        def __init__(self,controller):
            QThread.__init__(self)
            self.controller = controller
        
        def run(self):
            while not self.isInterruptionRequested():
                if self.controller.sem.available() == 0:
                    self.controller.sem.acquire(1)
                time.sleep(0.5)
                self.update_gui.emit()
                if not self.controller.w_player.is_playing(): # if is paused or stopped
                    self.controller.window.btnPlayPause.setText(">")
                    self.controller.window.btnPlayPause.setStyleSheet('QPushButton {background-color: green; color: white;}') 
                    if not self.controller.w_player.is_paused: # if is stopped
                        self.controller.w_player.stop()
                        if self.controller.m_player.player_preferences["loop_video"]:
                            self.controller.play()
                        else:
                            self.controller.sem.acquire(1)
                
            
if __name__ == '__main__':
    c = Controller()