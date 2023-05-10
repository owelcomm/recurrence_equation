from kivy.app import App
from kivy.core.window import Window
from kivy.graphics import Rectangle
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.scrollview import ScrollView

from utils.display.homogene_window import HomWindow
from utils.display.inhom_window import InhomWindow
from utils.display.complex_window import ComplexWindow
from utils.display.question_random import RandomWindow


class Hub(GridLayout):
    # Grille contenant les options principales (boutons)
    def __init__(self,root, **kwargs):
        super().__init__(**kwargs)
        self.padding=[50,0,50,0] #todo ajuster la hauteur
        self.spacing = [0,30]
        self.cols = 1
        self.pos_hint = {"top":0.7}
        self.row_default_height = 80
        self.root = root
        self.simp = Button(text = "Générer une question homogène simple",height=160,size_hint_y=None)
        self.simp.on_press = self.root.switch_to_simple
        self.complex = Button(text = "Générer une question homogène complexe",height=160,size_hint_y=None)
        self.complex.on_press = self.root.switch_to_complex
        self.inhom = Button(text = "Générer une question non-homogène",height=160,size_hint_y=None)
        self.inhom.on_press = self.root.switch_to_inhom
        self.random = Button(text = "Générer une question aléatoire",height=160,size_hint_y=None)
        self.random.on_press = self.root.switch_to_random
        self.add_widget(self.simp)
        self.add_widget(self.complex)
        self.add_widget(self.inhom)
        self.add_widget(self.random)

class MainWindow(ScreenManager):
    # Gestionnaire d'écrans, dont l'écran initial est l'écran de choix d'options
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        hub = Screen(name="hub")
        hub.add_widget(Hub(self))
        self.add_widget(hub)

        #écran scrollable associé aux équations homogènes standard
        normal = Screen(name="normal")
        self.normalScrollContainer = GridLayout(cols=1, size_hint=(1, 1),padding=[0,35,0,0])
        self.normalscroll=ScrollView(bar_width=30,bar_pos_y="right",size_hint=(1, None), size=(Window.width, Window.height))
        self.mainwin=HomWindow(self)
        self.normalscroll.add_widget(self.mainwin)
        self.normalScrollContainer.add_widget(self.normalscroll)
        normal.add_widget(self.normalScrollContainer)
        self.add_widget(normal)

        #écran scrollable associé aux équations complèxes
        complex = Screen(name="complex")
        self.complexScrollContainer = GridLayout(cols=1, size_hint=(1, 1),padding=[0,35,0,0])
        self.complexscroll=ScrollView(bar_width=30,bar_pos_y="right",size_hint=(1, None), size=(Window.width, Window.height))
        self.complexwin=ComplexWindow(self)
        self.complexscroll.add_widget(self.complexwin)
        self.complexScrollContainer.add_widget(self.complexscroll)
        complex.add_widget(self.complexScrollContainer)
        self.add_widget(complex)

        #écran scrollable associé aux équations non-homogènes
        inhom = Screen(name="inhom")
        self.inhomScrollContainer = GridLayout(cols=1, size_hint=(1, 1),padding=[0,35,0,0])
        self.inhomscroll=ScrollView(bar_width=30,bar_pos_y="right",size_hint=(1, None), size=(Window.width, Window.height))
        self.inhomwin=InhomWindow(self)
        self.inhomscroll.add_widget(self.inhomwin)
        self.inhomScrollContainer.add_widget(self.inhomscroll)
        inhom.add_widget(self.inhomScrollContainer)
        self.add_widget(inhom)
        #self.current = "normal"

        #écran scrollable associé aux équations aléatoire
        random = Screen(name="random")
        self.randomScrollContainer = GridLayout(cols=1, size_hint=(1, 1),padding=[0,35,0,0])
        self.randomscroll=ScrollView(bar_width=30,bar_pos_y="right",size_hint=(1, None), size=(Window.width, Window.height))
        self.randomwin=RandomWindow(self)
        self.randomscroll.add_widget(self.randomwin)
        self.randomScrollContainer.add_widget(self.randomscroll)
        random.add_widget(self.randomScrollContainer)
        self.add_widget(random)


        with self.canvas.before :
            self.background = Rectangle(pos=self.pos,size=self.size,source="resources/background.png")

    def switch_to_simple(self):
        #Va à l'écran associé à une équation homogène standard
        self.current="normal"

    def switch_to_complex(self):
        #Va à l'écran associé à une équation complèxe
        self.current="complex"

    def switch_to_inhom(self):
        #Va à l'écran associé à une équation non-homogène
        self.current="inhom"

    def switch_to_random(self):
        #Va à l'écran associé à une question aléatoire
        self.current="random"
        if self.randomwin.opt.type==1 or self.randomwin.opt.type==2:
            self.randomwin.opt.gen_homogene()
        elif self.randomwin.opt.type==3:
            self.randomwin.opt.gen_inhomog()

    def switch_to_hub(self):
        #Revient à l'écrant initial
        self.current="hub"

    def on_size(self, *args):
        #Trigger à chaque fois que la taille de l'écran est modifiée
        self.background.pos=self.pos
        self.background.size=self.size
        self.normalscroll.size = self.size
        #self.complexscroll.size = self.size



class MainApp(App):
    #Application principale, racine prinpicale
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.title = "Recurrence"
        #Window.size = (1300, 800)

    def build(self):
        return MainWindow()

if __name__ == "__main__":
    MainApp().run()