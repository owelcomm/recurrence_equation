from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.uix.image import Image
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.widget import Widget

from utils.equation.equation import Equation
from utils.equation.latex_display import eq_to_png
import random

labelcolor = [0,0,0,1]


class RanDisplay(GridLayout):
    def __init__(self,root,  **kwargs):
        super().__init__(**kwargs)
        self.cols = 1
        self.size_hint_y=None
        self.row_default_height = 30
        self.root = root
        self.root.height = 60*2
        self.root.root.normalscroll.scroll_y = 1
        self.type = random.randint(1, 3)

    def gen_homogene(self):
        values = list(range(-5, -1)) + list(range(2, 5))
        self.degree = random.randint(2,3)

        self.roots=[]
        for i in range(self.degree):
            self.roots.append(random.choice(values))

        self.constants=[]
        for i in range(self.degree):
            self.constants.append(random.choice(values))

        self.eq = Equation(degree=self.degree, real_roots=self.roots)
        self.eq.generate_symbolic_poly()
        self.eq.generate_latex_poly()
        self.eq.update_coefs(self.constants)
        self.eq.generate_solution()
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
        self.root.height+=270+200
        self.nexthom = Button(text = "Afficher la solution",height=30,size_hint_y=None)
        self.nexthom.on_press = self.next_homog
        self.add_widget(self.nexthom)

    def next_homog(self):
        self.nexthom.disabled=True
        self.add_widget(Label(text="Solution de l'exercice : ", halign="center",height=30,size_hint_y=None, color = labelcolor,font_size='15sp'))
        text = "Les racines de l'équation caractéristique sont "
        for i in self.roots[0:-1] :
            text+=str(i)+", "
        text = text[:-2]
        text+= " et " + str(self.roots[-1])+"."
        self.add_widget(Label(text=text, halign="center",height=40,size_hint_y=None, color = labelcolor,font_size='20sp'))
        self.add_widget(Label(text="La solution générale est ", halign="center",height=40,size_hint_y=None, color = labelcolor,font_size='20sp'))
        i=Image(source="latex_tools/résolution.png",height=40,size_hint_y=None)
        i.reload()
        self.add_widget(i)
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

        self.add_widget(Label(text=resocoef, halign="center",height=40,size_hint_y=None, color = labelcolor,font_size='20sp'))
        self.add_widget(Widget(height=30))

        self.reset = Button(text = "Générer une nouvelle question",height=30,size_hint_y=None)
        self.reset.on_press = self.root.reset
        self.add_widget(self.reset)

    def gen_inhomog(self):
        values = list(range(-5, -1)) + list(range(2, 5))
        self.degree = random.randint(2,3)

        self.roots=[]
        for i in range(self.degree):
            self.roots.append(random.choice(values))

        self.constants=[]
        for i in range(self.degree):
            self.constants.append(random.choice(values))

        self.eq = Equation(degree=self.degree, real_roots=self.roots)
        self.eq.generate_symbolic_poly()
        self.solut = self.eq.generate_solut_part()
        eq_to_png(r"$"+self.solut.replace("**","^").replace("*",".")+"$","latex_tools/solution_particulière.png")
        self.eq.add_solut_part(self.solut)
        self.eq.generate_latex_poly()
        self.eq.generate_solut_part()
        self.eq.update_coefs(self.constants)
        self.eq.generate_solution()


        self.add_widget(Label(text="Énoncé de l'exercice : ", halign="center", height=30, size_hint_y=None, color=labelcolor,
                              font_size='15sp'))
        self.add_widget(
            Label(text="Résoudre le système d'équation de récurrence suivant :", halign="center", height=40, size_hint_y=None,
                  color=labelcolor, font_size='20sp'))
        i = Image(source="latex_tools/équation_de_récurrence.png", height=40, size_hint_y=None)
        i.reload()
        self.add_widget(i)
        i = Image(source="latex_tools/contraintes.png", height=self.degree * 35, size_hint_y=None)
        i.reload()
        self.add_widget(i)
        self.root.height += 35 * self.degree
        self.add_widget(Widget(height=30))
        self.root.height += 270 + 200
        self.nextinhom = Button(text = "Afficher la solution",height=30,size_hint_y=None)
        self.nextinhom.on_press = self.next_inhom
        self.add_widget(self.nextinhom)

    def next_inhom(self):
        self.nextinhom.disabled=True
        self.add_widget(Label(text="Solution de l'exercice : ", halign="center", height=30, size_hint_y=None, color=labelcolor,
                              font_size='15sp'))
        text = "Les racines de l'équation caractéristique sont "
        for i in self.roots[0:-1]:
            text += str(i) + ", "
        text = text[:-2]
        text += " et " + str(self.roots[-1]) + ", et une solution particulière est :"
        self.root.height += 30
        self.add_widget(Label(text=text, halign="center", height=40, size_hint_y=None, color=labelcolor, font_size='20sp'))
        i = Image(source="latex_tools/solution_particulière.png", height=30, size_hint=(0.5, None))
        self.add_widget(i)
        i.reload()

        self.add_widget(Label(text="La solution générale est ", halign="center", height=40, size_hint_y=None, color=labelcolor,
                              font_size='20sp'))
        i = Image(source="latex_tools/résolution.png", height=40, size_hint_y=None)
        i.reload()
        self.add_widget(i)
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

        self.add_widget(Label(text=resocoef, halign="center", height=40, size_hint_y=None, color=labelcolor, font_size='20sp'))
        self.add_widget(Widget(height=30))

        self.reset = Button(text="Générer une nouvelle question", height=30, size_hint_y=None)
        self.reset.on_press = self.root.reset
        self.add_widget(self.reset)


class RandomWindow(GridLayout):
    def __init__(self, root, **kwargs):
        super().__init__(**kwargs)
        self.padding=[50,40,300,40]
        self.cols = 1
        self.root = root
        self.opt=RanDisplay(self)
        self.add_widget(self.opt)
        self.size_hint=(1, None)


    def reset(self):
        self.remove_widget(self.opt)
        self.opt=RanDisplay(self)
        self.add_widget(self.opt)
        self.root.current="hub"
        #self.root.current = "normal"