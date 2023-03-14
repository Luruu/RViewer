''' 
    Model
'''

class Model():
    def __init__(self, back, forward):
        self.player = PlayerModel(back,forward)


class PlayerModel():
    def __init__(self, back, forward):
        self.ms_back = self.seconds_to_ms(back)
        self.ms_forward = self.seconds_to_ms(forward)
    
    def seconds_to_ms(self, seconds):
        return seconds * 1000








    

