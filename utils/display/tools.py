from kivy.uix.label import Label
from kivy.uix.popup import Popup


class DegreeDisplay(Popup):
    def __init__(self,message,**kwargs):
        super().__init__(**kwargs)
        self.size_hint_max_y=None
        self.title="Une entrée est invalide"
        self.content=Label(text=message)
        self.size_hint=(None,None)
        self.size=(800,100)
        self.separator_color=[0.2,0.7,0.2,1]

def warning(message):
    popup = DegreeDisplay(message)
    popup.open()
