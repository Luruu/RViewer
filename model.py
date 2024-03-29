''' 
    Model
'''

import datetime
import vlc
import json
import sys
import os.path

def _save_in_file(filename, dict):
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(dict, f)


class VideoModel():
    def __init__(self, player_preferences, path_program):

        self.timestamps = {}
        self.file_timestamps = os.path.join(path_program, "timestamps.json") 


        self.default_video_preferences = {
            "track_value" : player_preferences["track_value"],
            "load_pos": 0,
            "selected_sub_title": 1, # I have to change this value when I know if it is a number or an object.
            "volume_value" : 100 # I have to change this value when I know range.
        }

        self.video_preferences = {}

        self.file_video_preferences = os.path.join(path_program, "preferences", "video_preferences.json") 
        self.name_video = "" # this is the name into json file

        self.video_info = {} # Title, Artist, Duration, Rate, etc.

    # define video name into json and srt
    def set_namevideofile(self):
        self.name_video = self.video_info["Title"] + str(self.video_info["Duration"])


    def _load_by_file(self,filename,videoname): 
        if not os.path.isfile(filename):
            return False

        with open(filename, 'r') as z:
            json_file = json.load(z)
            if videoname in json_file:
                return json_file[videoname]
            else: # video is not in json file
                return False 
    

    def _load_video_preferences_by_file(self):
        self.video_preferences = self._load_by_file(self.file_video_preferences,self.name_video)
        return self.video_preferences != False
    
    def _load_timestamps_by_file(self):
        self.timestamps = self._load_by_file(self.file_timestamps,self.name_video)
        return self.timestamps != False
    

    def load_videotimestamps(self):
        if not os.path.isfile(self.file_timestamps):
            video_dict = {self.name_video: {}} # in {} i'll have a dict of titles and timestamps
            _save_in_file(self.file_timestamps, video_dict)

        video_timestamps_exist = self._load_timestamps_by_file()
        if not video_timestamps_exist:
            self.timestamps = {}
    
    def delete_timestamp(self,title):
        self.timestamps.pop(title)
        self.save_timestamps()


    def load_videopreferences(self):
        #if file does not exists I have to create it and to set default values for a single video
        if not os.path.isfile(self.file_video_preferences):
            video_dict = {self.name_video: {}}
            video_dict[self.name_video] = self.default_video_preferences
            _save_in_file(self.file_video_preferences, video_dict)

        # now file exists, so I can read user video preferences (and if not exist video preferences, I use default video preferences )
        video_preferences_exist = self._load_video_preferences_by_file()
        if not video_preferences_exist:
            self.video_preferences = self.default_video_preferences 


    def add_timestamp(self,title,timestamp):
        self.timestamps[title] = timestamp
        self.save_timestamps()
    
    
    def save_timestamps(self):
        self._append_in_json(self.timestamps, self.file_timestamps)
    

    def save_video_preferences(self,track_pos,load_pos, vol, sel_sub):
        self.video_preferences = {
            "track_value" : track_pos,
            "load_pos": load_pos,
            "selected_sub_title": sel_sub, 
            "volume_value" : vol
        }
        self._append_in_json(self.video_preferences, self.file_video_preferences)
    
    def _append_in_json(self, subset, file_name): #add a subset (I mean a {"namevideo1": number1, "namevideo2": number2, etc. }) into a json

        # read all json file because I need all json to modify a single value of a key.
        with open(file_name, 'r') as z:
            self.file_json = json.load(z)

        self.file_json[self.name_video] = subset
        _save_in_file(file_name, self.file_json)
    
  
    def get_videoinfo_byvideo(self, w_player):
        for key, value in vlc.Meta._enum_names_.items():
            self.video_info[value] = w_player.get_video_property(vlc.Meta(key))
        
        self.video_info["Subs"] = { "Count": w_player.get_sub_count(),
                                            "available" : w_player.get_sub(),
                                            "descriptions": w_player.get_sub_descriptions()}
        self.video_info["Rate"] = w_player.get_rate()
        self.video_info["Duration"] = w_player.get_duration()
        self.video_info["Duration_ss"] = w_player.get_duration() / 1000
        self.video_info["Duration_hh_mm_ss"] = self.convert_ms_to_hmmss(w_player.get_duration())

    def convert_seconds_to_ms(self, seconds):
        return int(seconds) * 1000
    
    def convert_ms_to_hmmss(self, ms):
        return str(datetime.timedelta(seconds=int(ms/1000)))
    
    def convert_hmmss_to_ms(self,time_str):
        h, m, s = time_str.split(':')
        return str((int(h) * 3600 + int(m) * 60 + int(s)) * 1000)
    

   
class PlayerModel():
    def __init__(self, path_program):
        self.default_player_preferences = {
            "back_value" : 10,
            "forward_value" : 30,
            "track_value": 5,
            "loop_video": True,
            "pick_up_where_you_left_off": True,
            "track_video" : True,
            "show_subtitle_if_available" : True,
            "back_shortkey" : "Ctrl+D",
            "playpause_shortkey" : "Space",
            "forward_shortkey" : "Ctrl+G",
            "windows_dark_mode": sys.platform == "win32",
            "whisper_language": "english",
            "whisper_model": "base",
            "x" : 0,
            "y": 0,
            "dim": 0,
            "hei": 0,
            "show_time_stamp": True
        }

        self.player_preferences = {}

        self.file_player_preferences = os.path.join(path_program, "preferences", "player_preferences.json") 

        

        if not os.path.isfile(self.file_player_preferences): #If player file does not exists
            self.save_preferences_in_file(self.file_player_preferences, self.default_player_preferences) #create a file with default values

        with open(self.file_player_preferences, 'r') as f: 
            self.player_preferences = json.load(f) #update player preferences values with player_preferences.json 
        
    def save_player_preferences(self,back=None,forward=None,track_pos=None,loop=None,pick=None,save=None,show=None,x=None,y=None,dim=None,hei=None, back_short=None, plpau_short=None, forwd_short=None,darkmodewin=None, whisper_len=None, whisper_model=None, time_stamp=None):
        if back is not None:
            self.player_preferences["back_value"] = back
        if forward is not None:
            self.player_preferences["forward_value"] = forward
        if track_pos is not None:
            self.player_preferences["track_value"] = track_pos
        if loop is not None:
            self.player_preferences["loop_video"] = loop
        if pick is not None:
            self.player_preferences["pick_up_where_you_left_off"] = pick
        if save is not None:
            self.player_preferences["track_video"] = save
        if show is not None:
            self.player_preferences["show_subtitle_if_available"] = show
        if x is not None:
            self.player_preferences["x"] = x
        if y is not None:
            self.player_preferences["y"] = y
        if dim is not None:
            self.player_preferences["dim"] = dim
        if hei is not None:
            self.player_preferences["hei"] = hei

        if back_short is not None:
            self.player_preferences["back_shortkey"] = back_short
        if plpau_short is not None:
            self.player_preferences["playpause_shortkey"] = plpau_short
        if forwd_short is not None:
            self.player_preferences["forward_shortkey"] = forwd_short

        if darkmodewin is not None:
            self.player_preferences["windows_dark_mode"] = darkmodewin

        if whisper_len is not None:
            self.player_preferences["whisper_language"] = whisper_len
        
        if whisper_model is not None:
            self.player_preferences["whisper_model"] = whisper_model

        if time_stamp is not None:
            self.player_preferences["show_time_stamp"] = time_stamp

        # note: all key-values are salved into file. i.e: if back is None, self.player_preferences["back_value"] value is saved into file. If it is not none, back value instead is saved into file!
        _save_in_file(self.file_player_preferences, self.player_preferences)

    
    