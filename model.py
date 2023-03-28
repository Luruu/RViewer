''' 
    Model
'''

import datetime
import vlc
import json
import os.path


class VideoModel():
    def __init__(self):
        self.default_video_preferences = {
            "track_value" : 5,
            "load_pos": 0,
            "selected_sub_title": 1, # I have to change this value when I know if it is a number or an object.
            "volume_value" : 100 # I have to change this value when I know range.
        }

        self.video_preferences = {}

        self.file_video_preferences = "video_preferences.json"
        self.name_video = "" # this is the name into json file


        self.video_info = {} #Title, Artist, Duration, Rate, etc.
        
        

    def load_video_preferences_by_file(self, filename, videoname):
        with open(filename, 'r') as z:
            json_file = json.load(z)
            if videoname in json_file:
                self.video_preferences = json_file[videoname]
                return True
            else:
                return False
    

    def save_video_preferences_in_file(self, filename, dict):
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(dict, f)

    def load_videopreferences(self):
        self.name_video = self.video_info["Title"] + str(self.video_info["Duration"])
        
        #if file does not exists I have to create it and to set default values for a single video
        if not os.path.isfile(self.file_video_preferences):
            video_dict = {self.name_video: {}}
            video_dict[self.name_video] = self.default_video_preferences
            self.save_video_preferences_in_file(self.file_video_preferences, video_dict)

        # now file exists, so I can read user video preferences (and if not exist video preferences, into )
        video_preferences_exist = self.load_video_preferences_by_file(self.file_video_preferences, self.name_video)
        if not video_preferences_exist:
            self.video_preferences = self.default_video_preferences 
       
        
    def save_video_preferences(self,track_pos,load_pos, vol):
        self.video_preferences = {
            "track_value" : track_pos,
            "load_pos": load_pos,
            "selected_sub_title": 1, # I have to change this value when I know if it is a number or an object.
            "volume_value" : vol # I have to change this value when I know range.
        }

        # read all json file because I need all json to modify a single value of a key.
        with open(self.file_video_preferences, 'r') as z:
            self.file_json = json.load(z)

        self.file_json[self.name_video] = self.video_preferences
        self.save_video_preferences_in_file(self.file_video_preferences, self.file_json)
    
  
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
    

   
class PlayerModel():
    def __init__(self):
        self.default_player_preferences = {
            "back_value" : -10,
            "forward_value" : +30,
            "track_value": 5,
            "label_track_value": " 1.0x",
            "play_at_start": True,
            "loop_video": True,
            "pick_up_where_you_left_off": True,
            "save_track_value_on_close" : True,
            "show_subtitle_if_available" : True
        }

        self.player_preferences = {}

        self.file_player_preferences = "player_preferences.json"

        if not os.path.isfile(self.file_player_preferences): #If player file does not exists
            self.save_preferences_in_file(self.file_player_preferences, self.default_player_preferences) #create a file with default values

        with open(self.file_player_preferences, 'r') as f: 
            self.player_preferences = json.load(f) #update player preferences values with player_preferences.json 
        
    def save_player_preferences(self,play=None,back=None,forward=None,track_pos=None,load_pos=None,loop=None,pick=None,save=None,show=None):
        if play is not None:
            self.player_preferences["play_at_start"] = play
        if back is not None:
            self.player_preferences["back_value"] = back
        if forward is not None:
            self.player_preferences["forward_value"] = forward
        if track_pos is not None:
            self.player_preferences["track_value"] = track_pos
        if load_pos is not None:
            self.player_preferences["load_position"] = load_pos
        if loop is not None:
            self.player_preferences["loop_video"] = loop
        if pick is not None:
            self.player_preferences["pick_up_where_you_left_off"] = pick
        if save is not None:
            self.player_preferences["save_track_value_on_close"] = save
        if show is not None:
            self.player_preferences["show_subtitle_if_available"] = show

        self.save_preferences_in_file(self.file_player_preferences, self.player_preferences)

    
    def save_preferences_in_file(self, filename, dict):
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(dict, f)