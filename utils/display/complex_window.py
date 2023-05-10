from kivy.uix.button import Button
from kivy.uix.dropdown import DropDown
from kivy.uix.gridlayout import GridLayout
from kivy.uix.image import Image
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.widget import Widget

from utils.display.tools import warning
from utils.equation.equation import Equation
from utils.equation.latex_display import eq_to_png

import math

labelcolor = [0,0,0,1]

class DegreeDisplay(GridLayout):
    def __init__(self,root,**kwargs):
        super().__init__(**kwargs)
        self.root=root
        self.size_hint_max_y=None
        self.cols=2
        self.degree = TextInput(text = "", halign="center", multiline=False,height=30,size_hint=(0.7,None))
        self.add_widget(self.degree)
        self.ok = Button(text = "ok",height=30,size_hint_y=None,size_hint_x=0.3,halign="right")
        self.ok.on_press = self.next
        self.add_widget(self.ok)
    def next(self):
        try:
            self.root.degree = int(self.degree.text)
            self.root.next_step()
        except:
            warning("Le degré doit être un entier.")

class RootRequest(GridLayout):
    def __init__(self,root,degree,**kwargs):
        super().__init__(**kwargs)
        self.degree=degree
        self.root=root
        self.height=30
        self.size_hint_max_y=None
        self.cols=2
        npossible_roots = degree//2+1
        possible_roots = [str(i*2) for i in range(npossible_roots)]
        self.dropdown = DropDown()
        for i in possible_roots:
            btn = Button(text=i,height=30,size_hint=(0.7,None),halign="right")
            btn.bind(on_release=lambda btn: self.dropdown.select(btn.text))
            self.dropdown.add_widget(btn)
        self.dropdown.bind(on_select=lambda instance, x : self.set_arg(x))

        self.mainBut = Button(text = possible_roots[0],height=30,size_hint=(0.7,None),halign="right")
        self.mainBut.bind(on_release=self.dropdown.open)
        self.add_widget(self.mainBut)

        self.ok = Button(text = "ok",height=30,size_hint_y=None,size_hint_x=0.3,halign="right")
        self.ok.on_press = self.next
        self.add_widget(self.ok)

    def set_arg(self,x):
        self.mainBut.text = x
    def next(self):
        self.root.nrroots = self.degree-int(self.mainBut.text)
        self.root.ncroots = int(self.mainBut.text)
        self.root.next_step()

class RealRootDisplay(GridLayout):
    def __init__(self,root,degree,**kwargs):
        super().__init__(**kwargs)
        self.root=root
        self.height=30
        self.size_hint_max_y=None
        self.cols=degree+1
        self.roots=[]
        for i in range(degree):
            self.roots.append(TextInput(text = "", halign="center", multiline=False,height=30,size_hint=(0.7/degree,None)))
            self.add_widget(self.roots[-1])
        self.ok = Button(text = "ok",height=30,size_hint_y=None,size_hint_x=0.3,halign="right")
        self.ok.on_press = self.next
        self.add_widget(self.ok)

    def next(self):
        try:
            formatNumber = lambda n: n if n % 1 else int(n)
            self.root.real_roots = [formatNumber(float(i.text)) for i in self.roots]
            self.root.next_step()
        except:
            warning("Une racine n'a pas été correctement lue. Attention à noter les fractions sous leur forme décimale.")




class moduleDisplay(GridLayout):
    def __init__(self,root,**kwargs):
        super().__init__(**kwargs)
        self.root=root
        self.height=30
        self.size_hint_max_y=None
        self.cols=2
        self.module = TextInput(text = "", halign="center", multiline=False,height=30,size_hint=(0.7,None))
        self.add_widget(self.module)
        self.ok = Button(text = "ok",height=30,size_hint_y=None,size_hint_x=0.3,halign="right")
        self.ok.on_press = self.next
        self.add_widget(self.ok)
    def next(self):
        try:
            mod=float(self.module.text)
            formatNumber = lambda n: n if n % 1 else int(n)
            self.root.mod = formatNumber(mod)
            self.root.next_step()
        except:
            warning("le module n'a pas été correctement lu. Attention à noter les fractions sous leur forme décimale.")

class argDisplay(GridLayout):
    def __init__(self,root,**kwargs):
        super().__init__(**kwargs)
        self.root=root
        self.height=30
        self.size_hint_max_y=None
        self.cols=2


        self.angles = ["0","π/6","π/4","π/3","π/2","2π/3","3π/4","5π/6","π","7π/6","5π/4","4π/3","3π/2","5π/3","7π/4","11π/6"]
        self.anglesalt = [(0,1),(1,6),(1,4),(1,3),(1,2),(2,3),(3,4),(5,6),(1,1),(7,6),(5,4),(4,3),(3,2),(5,3),(7,4),(11,6)]
        self.dropdown = DropDown()
        for i in self.angles:
            btn = Button(text=i,height=30,size_hint=(0.7,None),halign="right")
            btn.bind(on_release=lambda btn: self.dropdown.select(btn.text))
            self.dropdown.add_widget(btn)
        self.dropdown.bind(on_select=lambda instance, x : self.set_arg(x))

        self.mainBut = Button(text = "0",height=30,size_hint=(0.7,None),halign="right")
        self.mainBut.bind(on_release=self.dropdown.open)
        self.add_widget(self.mainBut)


        self.ok = Button(text = "ok",height=30,size_hint_y=None,size_hint_x=0.3,halign="right")
        self.ok.on_press = self.next
        self.add_widget(self.ok)


    def set_arg(self,x):
        self.mainBut.text = x

    def next(self):
        self.root.arg = self.anglesalt[self.angles.index(self.mainBut.text)]
        self.root.eq.add_complex_roots((self.root.mod,self.root.arg))
        self.root.next_step()



class ConstantDisplay(GridLayout):
    def __init__(self,root,degree,**kwargs):
        super().__init__(**kwargs)
        self.root=root
        self.height=30
        self.size_hint_max_y=None
        self.cols=degree+1
        self.const=[]
        for i in range(degree):
            self.const.append(TextInput(text = "", halign="center", multiline=False,height=30,size_hint=(0.7/degree,None)))
            self.add_widget(self.const[-1])
        self.ok = Button(text = "ok",height=30,size_hint_y=None,size_hint_x=0.3,halign="right")
        self.ok.on_press = self.next
        self.add_widget(self.ok)

    def next(self):
        try:
            formatNumber = lambda n: n if n % 1 else int(n)
            self.root.constants = [formatNumber(float(i.text)) for i in self.const]
            self.root.next_step()
        except:
            warning("Un coefficient n'a pas été correctement lu. Attention à noter les fractions sous leur forme décimale.")


class ComplexDisplay(GridLayout):
    def __init__(self,root,  **kwargs):
        super().__init__(**kwargs)
        self.cols = 1
        self.size_hint_y=None
        self.row_default_height = 30
        self.root = root
        self.add_widget(Label(text="Degré : ", halign="center",height=30,size_hint_y=None, color = labelcolor))
        self.degree_win = DegreeDisplay(self)
        self.add_widget(self.degree_win)
        self.root.height = 60*2
        self.state = "degree"
        self.root.root.normalscroll.scroll_y = 1
        self.crootdone=0
        self.arg=0
        self.mod=0

    def next_step(self):
        if self.state == "degree":
            self.add_widget(Label(text="Nombre de racines complexes : ", halign="center",height=30,size_hint_y=None, color = labelcolor))
            self.rootreq = RootRequest(self,self.degree)
            self.add_widget(self.rootreq)
            self.state="choose_roots"


        elif self.state == "choose_roots":
            self.add_widget(Label(text="Racines réelles: ", halign="center",height=30,size_hint_y=None, color = labelcolor))
            self.roots_win = RealRootDisplay(self,self.nrroots)
            self.add_widget(self.roots_win)
            self.root.height += 90
            self.state = "roots_real"

        elif self.state == "roots_real":
            self.eq = Equation(degree=self.degree, real_roots=self.real_roots, isComplex=self.ncroots!=0, complex_roots=[])
            self.state = "roots_mod"
            self.next_step()

        elif self.state == "roots_mod":
            if self.crootdone<self.ncroots:
                if self.crootdone==0:
                    self.add_widget(Widget())
                    eq = r"Format des complexes : $a+bi$ et $a-bi$"
                    eq_to_png(eq,"latex_tools/solutions.png")
                    i=Image(source="latex_tools/solutions.png",height=30,size_hint_y=None)
                    i.reload()
                    self.add_widget(i)

                    eq = r"$a=\rho\cos\Theta$ et $b=\rho\sin\Theta$"
                    eq_to_png(eq,"latex_tools/ab.png")
                    i=Image(source="latex_tools/ab.png",height=30,size_hint_y=None)
                    i.reload()
                    self.add_widget(i)
                    self.root.height += 120


                self.add_widget(Widget())
                self.add_widget(Label(text="Choix de la paire de racines complexes suivante : ", halign="center",height=30,size_hint_y=None, color = labelcolor))
                self.root.height += 90
                self.add_widget(Label(text="Choix du module du complexe (ρ): ", halign="center", height=30, size_hint_y=None,color=labelcolor))
                self.module = moduleDisplay(self)
                self.add_widget(self.module)
                self.root.height += 60
                self.state = "roots_arg"
            else :
                self.state = "complex_roots"
                self.next_step()

        elif self.state =="roots_arg":
            self.add_widget(Label(text="Choix de l'argument du complexe (Θ) :", halign="center", height=30, size_hint_y=None, color=labelcolor))
            self.argdisp = argDisplay(self)
            self.add_widget(self.argdisp)
            self.root.height += 60
            self.state = "roots_mod"
            self.crootdone+=2


        elif self.state =="complex_roots":
            self.eq.generate_symbolic_poly()
            self.eq.generate_latex_poly()
            self.add_widget(Label(text="Polynôme caractéristique factorisé :", halign="center",height=30,size_hint_y=None, color = labelcolor))
            i=Image(source="latex_tools/polynome_factorisé.png",height=40,size_hint_y=None)
            i.reload()
            self.add_widget(i)
            self.add_widget(Label(text="Polynôme caractéristique non-factorisé :", halign="center",height=30,size_hint_y=None, color = labelcolor))
            i=Image(source="latex_tools/polynome_non_factorisé.png",height=30,size_hint_y=None)
            i.reload
            self.add_widget(i)
            self.add_widget(Label(text="Équation de récurrence :", halign="center",height=30,size_hint_y=None, color = labelcolor,font_size='20sp'))
            i=Image(source="latex_tools/équation_de_récurrence_highlight.png",height=60,size_hint_y=None)
            i.reload()
            self.add_widget(i)
            self.add_widget(Label(text="Résolution :", halign="center",height=30,size_hint_y=None, color = labelcolor))
            i=Image(source="latex_tools/résolution.png",height=40,size_hint_y=None)
            i.reload()
            self.add_widget(i)
            self.add_widget(Label(text="Choix des coefficients (a, b, c, ...) :", halign="center",height=30,size_hint_y=None, color = labelcolor))
            self.consts = ConstantDisplay(self,self.degree)
            self.add_widget(self.consts)
            self.root.height += 360
            self.state = "constants"


        elif self.state =="constants":
            self.eq.update_coefs(self.constants)
            self.eq.generate_solution()
            self.add_widget(Widget(height=30))
            self.add_widget(Label(text="Énoncé de l'exercice : ", halign="center",height=30,size_hint_y=None, color = labelcolor,font_size='15sp'))
            self.add_widget(Label(text="Résoudre le système d'équation de récurrence suivant :", halign="center",height=40,size_hint_y=None, color = labelcolor,font_size='20sp'))
            i=Image(source="latex_tools/équation_de_récurrence.png",height=40,size_hint_y=None)
            i.reload()
            self.add_widget(i)
            i=Image(source="latex_tools/contraintes.png",height=self.degree*35,size_hint_y=None)
            i.reload()
            self.add_widget(i)
            self.root.height += 35*self.degree
            self.add_widget(Widget(height=30))
            self.root.height+=270
            #self.add_widget(Label(text="Solution de l'exercice : ", halign="center",height=30,size_hint_y=None, color = labelcolor,font_size='15sp'))
            #Todo faire la résolution
            #text = "Les racines de l'équation caractéristique sont "
            #for i in self.roots[0:-1] :
            #    text+=str(i)+", "
            #text = text[:-2]
            #text+= " et " + str(self.roots[-1])+"."
            #self.add_widget(Label(text=text, halign="center",height=40,size_hint_y=None, color = labelcolor,font_size='20sp'))
            #self.add_widget(Label(text="La solution générale est ", halign="center",height=40,size_hint_y=None, color = labelcolor,font_size='20sp'))
            #i=Image(source="latex_tools/résolution.png",height=40,size_hint_y=None)
            #i.reload()
            #self.add_widget(i)
            #alphab = [chr(i) for i in range(ord('a'), ord('z') + 1)]
            #resocoef = "où "
            #for i in range(len(self.constants)):
            #    if i == 0:
            #        resocoef += alphab[i] + "=" + str(self.constants[i])
            #    else:
            #        if i != len(self.roots) - 1:
            #            resocoef += ", " + alphab[i] + "=" + str(self.constants[i])
            #        else:
            #            resocoef += " et " + alphab[i] + "=" + str(self.constants[i])

            #self.add_widget(Label(text=resocoef, halign="center",height=40,size_hint_y=None, color = labelcolor,font_size='20sp'))
            self.add_widget(Widget(height=30))

            self.reset = Button(text = "Générer une nouvelle question",height=30,size_hint_y=None)
            self.reset.on_press = self.root.reset
            self.latex = Button(text = "Générer le fichier latex",height=30,size_hint_y=None)
            self.latex.on_press = self.eq.generate_latex_file
            self.add_widget(self.latex)
            self.add_widget(self.reset)





class ComplexWindow(GridLayout):
    def __init__(self, root, **kwargs):
        super().__init__(**kwargs)
        self.padding=[50,40,300,40]
        self.cols = 1
        self.root = root
        self.opt=ComplexDisplay(self)
        self.add_widget(self.opt)
        self.size_hint=(1, None)


    def reset(self):
        self.remove_widget(self.opt)
        self.opt=ComplexDisplay(self)
        self.add_widget(self.opt)
        self.root.current="hub"
        #self.root.current = "normal"