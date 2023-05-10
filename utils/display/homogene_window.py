from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.uix.image import Image
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.widget import Widget

from utils.display.tools import warning
from utils.equation.equation import Equation

labelcolor = [0,0,0,1]

class DegreeDisplay(GridLayout):
    def __init__(self,root,**kwargs):
        super().__init__(**kwargs)
        self.root=root
        self.size_hint_max_y=None
        self.cols=2
        self.degree = TextInput(text = "", halign="center", multiline=False,height=120,size_hint=(0.7,None))
        self.add_widget(self.degree)
        self.ok = Button(text = "ok",height=120,size_hint_y=None,size_hint_x=0.3,halign="right")
        self.ok.on_press = self.next
        self.add_widget(self.ok)
    def next(self):
        try:
            self.root.degree = int(self.degree.text)
            self.root.next_step()
        except:
            warning("Le degré doit être un entier.")


class RootDisplay(GridLayout):
    def __init__(self,root,degree,**kwargs):
        super().__init__(**kwargs)
        self.root=root
        self.height=90
        self.size_hint_max_y=None
        self.cols=degree+1
        self.roots=[]
        for i in range(degree):
            self.roots.append(TextInput(text = "", halign="center", multiline=False,height=120,size_hint=(0.7/degree,None)))
            self.add_widget(self.roots[-1])
        self.ok = Button(text = "ok",height=120,size_hint_y=None,size_hint_x=0.3,halign="right")
        self.ok.on_press = self.next
        self.add_widget(self.ok)

    def next(self):
        try:
            formatNumber = lambda n: n if n % 1 else int(n)
            self.root.roots = [formatNumber(float(i.text)) for i in self.roots]
            self.root.next_step()
        except:
            warning("Une racine n'a pas été correctement lue. Attention à noter les fractions sous leur forme décimale.")

class ConstantDisplay(GridLayout):
    def __init__(self,root,degree,**kwargs):
        super().__init__(**kwargs)
        self.root=root
        self.height=90
        self.size_hint_max_y=None
        self.cols=degree+1
        self.const=[]
        for i in range(degree):
            self.const.append(TextInput(text = "", halign="center", multiline=False,height=120,size_hint=(0.7/degree,None)))
            self.add_widget(self.const[-1])
        self.ok = Button(text = "ok",height=120,size_hint_y=None,size_hint_x=0.3,halign="right")
        self.ok.on_press = self.next
        self.add_widget(self.ok)

    def next(self):
        try:
            formatNumber = lambda n: n if n % 1 else int(n)
            self.root.constants = [formatNumber(float(i.text)) for i in self.const]
            self.root.next_step()
        except:
            warning("Un coefficient n'a pas été correctement lu. Attention à noter les fractions sous leur forme décimale.")


class HomDisplay(GridLayout):
    def __init__(self,root,  **kwargs):
        super().__init__(**kwargs)
        self.cols = 1
        self.size_hint_y=None
        self.row_default_height = 120
        self.root = root
        self.add_widget(Label(text="Degré : ", halign="center",height=90,size_hint_y=None, color = labelcolor))
        self.degree_win = DegreeDisplay(self)
        self.add_widget(self.degree_win)
        self.root.height = 120*2
        self.state = "degree"
        self.root.root.normalscroll.scroll_y = 1

    def next_step(self):
        if self.state == "degree":
            self.add_widget(Label(text="Racines : ", halign="center",height=90,size_hint_y=None, color = labelcolor))
            self.roots_win = RootDisplay(self,self.degree)
            self.add_widget(self.roots_win)
            self.root.height += 240
            self.state = "roots"

        elif self.state =="roots":
            self.eq = Equation(degree=self.degree, real_roots=self.roots)
            self.eq.generate_symbolic_poly()
            self.eq.generate_latex_poly()
            self.add_widget(Label(text="Polynôme caractéristique factorisé :", halign="center",height=90,size_hint_y=None, color = labelcolor))
            i=Image(source="latex_tools/polynome_factorisé.png",height=90,size_hint_y=None)
            i.reload()
            self.add_widget(i)
            self.add_widget(Label(text="Polynôme caractéristique non-factorisé :", halign="center",height=90,size_hint_y=None, color = labelcolor))
            i=Image(source="latex_tools/polynome_non_factorisé.png",height=90,size_hint_y=None)
            i.reload
            self.add_widget(i)
            self.add_widget(Label(text="Équation de récurrence :", halign="center",height=90,size_hint_y=None, color = labelcolor,font_size='15sp'))
            i=Image(source="latex_tools/équation_de_récurrence_highlight.png",height=90,size_hint_y=None)
            i.reload()
            self.add_widget(i)
            self.add_widget(Label(text="Résolution :", halign="center",height=90,size_hint_y=None, color = labelcolor))
            i=Image(source="latex_tools/résolution.png",height=90,size_hint_y=None)
            i.reload()
            self.add_widget(i)
            self.add_widget(Label(text="Choix des coefficients (a, b, c, ...) :", halign="center",height=90,size_hint_y=None, color = labelcolor))
            self.consts = ConstantDisplay(self,self.degree)
            self.add_widget(self.consts)
            self.root.height += 9*120+240
            self.state = "constants"


        elif self.state =="constants":
            self.eq.update_coefs(self.constants)
            self.eq.generate_solution()
            self.add_widget(Widget(height=90))
            self.add_widget(Label(text="Énoncé de l'exercice : ", halign="center",height=90,size_hint_y=None, color = labelcolor,font_size='15sp'))
            self.add_widget(Label(text="Résoudre le système d'équation de récurrence suivant :", halign="center",height=90,size_hint_y=None, color = labelcolor,font_size='15sp'))
            i=Image(source="latex_tools/équation_de_récurrence.png",height=90,size_hint_y=None)
            i.reload()
            self.add_widget(i)
            i=Image(source="latex_tools/contraintes.png",height=self.degree*60,size_hint_y=None)
            i.reload()
            self.add_widget(i)
            self.root.height += 60*self.degree
            self.add_widget(Widget(height=90))
            self.root.height+=120*5 #todo ajuster la hauteur
            self.add_widget(Label(text="Solution de l'exercice : ", halign="center",height=90,size_hint_y=None, color = labelcolor,font_size='15sp'))
            text = "Les racines de l'équation caractéristique sont "
            for i in self.roots[0:-1] :
                text+=str(i)+", "
            text = text[:-2]
            text+= " et " + str(self.roots[-1])+"."
            self.add_widget(Label(text=text, halign="center",height=90,size_hint_y=None, color = labelcolor,font_size='15sp'))
            self.add_widget(Label(text="La solution générale est ", halign="center",height=90,size_hint_y=None, color = labelcolor,font_size='15sp'))
            i=Image(source="latex_tools/résolution.png",height=90,size_hint_y=None)
            i.reload()
            self.add_widget(i)
            self.root.height+=120*4 #todo ajuster la hauteur

            alphab = [chr(i) for i in range(ord('a'), ord('z') + 1)]
            resocoef = "où "
            for i in range(len(self.constants)):
                if i == 0:
                    resocoef += alphab[i] + "=" + str(self.constants[i])
                else:
                    if i != len(self.roots) - 1:
                        resocoef += ", " + alphab[i] + "=" + str(self.constants[i])
                    else:
                        resocoef += " et " + alphab[i] + "=" + str(self.constants[i])

            self.add_widget(Label(text=resocoef, halign="center",height=90,size_hint_y=None, color = labelcolor,font_size='15sp'))
            self.add_widget(Widget(height=90))

            self.reset = Button(text = "Générer une nouvelle question",height=120,size_hint_y=None)
            self.reset.on_press = self.root.reset
            self.latex = Button(text = "Générer le fichier latex",height=120,size_hint_y=None)
            self.latex.on_press = self.eq.generate_latex_file
            self.root.height+=120*4 #todo ajuster la hauteur
            self.add_widget(self.latex)
            self.add_widget(self.reset)





class HomWindow(GridLayout):
    def __init__(self, root, **kwargs):
        super().__init__(**kwargs)
        self.padding=[50,40,50,40]
        self.cols = 1
        self.root = root
        self.opt=HomDisplay(self)
        self.add_widget(self.opt)
        self.size_hint=(1, None)


    def reset(self):
        self.remove_widget(self.opt)
        self.opt=HomDisplay(self)
        self.add_widget(self.opt)
        self.root.current="hub"
        #self.root.current = "normal"