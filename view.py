'''
    view
'''

from PySide6.QtCore import QStandardPaths, Qt, Slot, QUrl
from PySide6.QtGui import QAction, QIcon, QKeySequence, QScreen, QPalette, QColor
from PySide6.QtWidgets import (QApplication, QDialog, QFileDialog,QWidget,
    QMainWindow, QSlider, QStyle, QToolBar, QLabel, QFrame, QPushButton, QSizePolicy)



import vlc
import sys


class View():
    def __init__(self, source_path):
        self.player = PlayerView(source_path)
        self.window = WindowView(self.player.get_istance_vlc_player())
         

class PlayerView():
    def __init__(self, video_path):
        self.video_path = video_path
        self.vlc_istance = vlc.Instance()
        self.vlc_player = self.vlc_istance.media_player_new()
        self.media = self.vlc_istance.media_new(video_path)
        self.vlc_player.set_media(self.media)
        self.video_info = {"duration" : self.vlc_player.get_length(), 
                      "rate" : self.vlc_player.get_rate()}
        
    

    def get_istance_vlc_player(self):
        return self.vlc_player
        
    def set_subtitle(self, subtitle_path):
        self.vlc_player.video_set_subtitle_file(subtitle_path)
    
    def play(self):
        return self.vlc_player.play()
    
    def pause(self):
        return self.vlc_player.pause()
    
    def stop(self):
        return self.vlc_player.stop()
    
    def is_playing(self):
        return self.vlc_player.is_playing()
    
    def go_back(self, ms):
        new_pos = self.get_time() - ms
        print("a",self.get_time())
        if new_pos >=0:
            self.set_time(new_pos)
        else:
            self.stop()
            self.play()
        
    
    def go_forward(self, ms):
        # self.pause()
        new_pos = self.get_time() + ms 
        duration = self.get_duration()
        print("b",new_pos, duration)
        if new_pos < duration:
            self.set_time(new_pos)

    def get_state(self):
        return self.vlc_player.get_state()
    
    def get_duration(self):
        return self.vlc_player.get_length()
    
    def get_time(self):
        return self.vlc_player.get_time()
    
    def set_time(self, i_time):
        return self.vlc_player.set_time(i_time)
    
    def get_position(self):
        return self.vlc_player.get_position()
    
    def set_position(self, f_pos):
        return self.vlc_player.set_position(f_pos)
    
    def get_rate(self):
        return self.vlc_player.get_rate()
    
    def set_rate(self, rate):
        return self.vlc_player.set_rate(rate)
    
    def get_state(self):
        return self.vlc_player.get_state()
   
    
    '''
    to-do: 

    video_get_spu_count

    video_set_spu

    video_get_spu_delay

    video_set_spu_delay

    '''


class WindowView(QMainWindow):
    def __init__(self,player):
        self.app = QApplication(sys.argv)
        super().__init__()
        available_geometry = self.screen().availableGeometry()
        self.resize(available_geometry.width() / 4,
                        available_geometry.height() / 3.5)
        
        
        self.setWindowTitle("RViewer")
        
        self.videoframe = QFrame()
        # set videoframe color
        self.palette = self.videoframe.palette()
        self.palette.setColor(QPalette.Window, QColor(0, 0, 0))
        self.videoframe.setPalette(self.palette)
        self.videoframe.setAutoFillBackground(True)
        self.setCentralWidget(self.videoframe)

        self.tool_bar = QToolBar()
        self.tool_bar2 = QToolBar()
        #per far essere stacked le due toolbar
        

        self.addToolBar(Qt.BottomToolBarArea, self.tool_bar)
        self.addToolBarBreak(Qt.BottomToolBarArea)
        self.addToolBar(Qt.BottomToolBarArea, self.tool_bar2)



        self.btnBack = QPushButton(self)
        self.btnBack.setText("-10")          #text
        self.btnBack.setShortcut('Ctrl+D')  #shortcut key
        self.btnBack.move(100,100)
        



        self.btnForward = QPushButton(self)
        self.btnForward.setText("+30")          #text
        self.btnForward.setShortcut('Ctrl+F')  #shortcut key
        self.btnForward.move(100,100)
        


        

        self.anchorVLCtoWindow(player, self.videoframe.winId())
        
        



    def anchorVLCtoWindow(self, player, id):
        if sys.platform.startswith('linux'): # for Linux using the X Server
            player.set_xwindow(id)
        elif sys.platform == "win32": # for Windows
            player.set_hwnd(id)
        elif sys.platform == "darwin": # for MacOS
            player.set_nsobject(id)
        else:
            print("ERROR: this software does not work with", sys.platform)
        
        