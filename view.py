'''
    view
'''

import sys
from PySide6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QFrame
from PySide6.QtGui import QPalette, QColor
import vlc



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
    
    def is_playing(self):
        return self.vlc_player.is_playing()
    
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
        app = QApplication(sys.argv)
        super().__init__()
        available_geometry = self.screen().availableGeometry()
        self.resize(available_geometry.width() / 3,
                        available_geometry.height() / 2)
        
        
        if sys.platform.startswith('linux'): # for Linux using the X Server
            player.set_xwindow(int(self.winId()))
        elif sys.platform == "win32": # for Windows
            player.set_hwnd(self.winId())
        elif sys.platform == "darwin": # for MacOS
            player.set_nsobject(self.videoframe.winId())
        else:
            print("Errore: ", sys.platform)
        
        self.show()
        
        player.play()
        sys.exit(app.exec())
        
        