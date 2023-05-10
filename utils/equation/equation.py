import sympy
from sympy import Rational
import math
from utils.equation.latex_display import eq_to_png, highlight
from sympy.parsing.sympy_parser import parse_expr, standard_transformations, auto_number
import random as rd

from utils.equation.latex_file_generation import generate_start, generate_question, generate_solution, generate_end, \
    generate_solution_complex

alphabet = [chr(i) for i in range(ord('a'), ord('z') + 1)]
alphabet_maj = [chr(i) for i in range(ord('A'), ord('Z') + 1)]
formatNumber = lambda n: n if n % 1 else int(n)


# def isInteger(x):
#     if abs(x % 1) <= 0.00001 or abs(x % 1 - 1) <= 0.00001:
#         return True
#     else:
#         return False


class Equation:
    """
    Une classe pour représenter une équation

    self.degree : int
        degré de l'équation
    self.real_roots : list[real]
        liste composée des racines réelles de l'équation
    self.coefs_abc : list[real]
        liste composée des différents coefficients (a, b, c, ...) de l'équation
    self.coef_recurrence : list[real]
        liste composée des différents coefficients du polynôme associé à l'équation

    self.equations_symbolic_ref : dict
        dictionnaire associant à chaque expression importante sa traduction Sympy
    self.equations_latex_ref : dict
        dictionnaire associant à chaque expression importante sa traduction Latex

    self.isComplex : boolean
        True si l'équation a des racines complèxes, False sinon
    self.complex_roots : list[root]
        où root : tuple (module,argument)
            module : float
            argument : tuple (int,int) correspondant respectivement au numérateur et dénumérateur multipliant pi
                        par exemple, un argument de 3π/4 correspondra à (3,4)


    self.isInhom : boolean
        True si l'équation admet une partie non-homogène, false sinon
    self.inhom : Sympy expression
        expression sympy correspondant à la partie inhomogène simplifiée de l'équation
    self.solut_part : Str
        string contenant le membre correspondant à la solution particulière
    """

    def __init__(self, isComplex=False, degree=0, real_roots=None, complex_roots=None):
        if real_roots == None:
            real_roots = []
        if complex_roots == None:
            complex_roots = []

        self.isComplex = isComplex
        self.degree = degree
        self.real_roots = real_roots
        self.complex_roots = complex_roots
        self.equations_symbolic_ref = {}
        self.equations_latex_ref = {}
        self.coef_recurrence = []
        self.coefs_abc = []
        self.inhom = "0"
        self.isInhom = False

    def update_degree(self, degree):
        """ Tente de mettre à jour le degré de l'équation

        Parameters
        ----------
        degree : int
            Le nouveau degré de l'équation homogène associée

        Returns
        -------
        True si l'update du degré a bien été effectuée, False sinon

        Raises
        ------
        DegreeInputError (todo)
            Si on ne parvient pas à lire degree comme un entier
        """
        try:
            self.degree = int(degree)
            return True
        except:
            print("Could not read degree value")
            return False

    def update_real_roots(self, roots):
        """ Tente de mettre à jour les différentes racines réelles de l'équation

        Parameters
        ----------
        roots : list
            Une liste de réels correspondant aux différentes racines réelles de l'équation

        Returns
        -------
        True si l'update des racines a bien été effectuée, False sinon

        Raises
        ------
        RealRootInputError (todo)
            Si on ne parvient pas à lire les racines
        """
        try:
            roots = list(map(lambda r: float(r), roots))
            self.real_roots = roots
            return True
        except:
            print("Could not read real roots values")
            return False

    def add_complex_roots(self, root):
        """ Rajoute une racine complèxe à l'équation

        Parameters
        ----------
        root : tuple (module,argument)
            module : float
            argument : tuple (int,int) correspondant respectivement au numérateur et dénumérateur multipliant pi
                        par exemple, un argument de 3π/4 correspondra à (3,4). Ce choix a été fait, par rapport à un
                        float, afin de représenter de manière plus intuitive la fraction lors de la génération du
                        fichier latex
            Une racine complèxe à rajouter à la liste self.complex_roots de l'équation
        """
        print(self.complex_roots)
        self.complex_roots.append(root)

    def generate_solut_part(self):
        """ Génère aléatoirement une solution particulière

        Returns
        -------
        eq : str
            string correspondant une solution particulière générée aléatoirement parmis 3 types d'expressions :
                "a*n+b"
                "a*n**2+b*n+c"
                "a*b**n+c"
        """

        values = list(range(-5, -1)) + list(range(2, 6))  # Les valeurs possibles pour les paramètres a,b et c,
        # on enlève les 1 et 0 par simplicité pour éviter les potentielles simplifications nécessaires
        signvalues = ['-' + str(abs(i)) if i < 0 else '+' + str(abs(i)) for i in values]  # on rajoute le "-", ou le "+" devant la valeur des paramètres

        type = rd.randint(1, 5)  # On choisi le type d'équation aléatoirement
        print("type d'équation : ", type)
        if type == 1 or type == 2:  # an+b
            a_value = rd.choice(values)
            b_value = rd.choice(signvalues)
            eq = str(a_value) + "*n" + b_value
        elif type == 3 or type == 4:  # an²+bn+c
            a_value = rd.choice(values)
            b_value = rd.choice(signvalues)
            c_value = rd.choice(signvalues)
            eq = str(a_value) + "*n**2" + b_value + "*n" + c_value
        elif type == 5:  # ab^(n)+c
            a_value = rd.choice(values)
            b_value = abs(rd.choice(values))
            c_value = rd.choice(signvalues)
            eq = str(a_value) + "*" + str(b_value) + "**n" + c_value
        print("solution particulière : ", eq)
        return eq

    def add_solut_part(self, solution):
        """ Déclare l'équation inhomogène, rajoute sa solution particulière, et génère sa partie inhomogène

        self.isInhom devient True
        self.solut_part devient un string contenant le membre correspondant à la solution particulière
        self.inhom devient une expression sympy correspondant à la partie inhomogène simplifiée de l'équation

        Parameters
        ----------
        solution : str
            solution particulière ayant une des formes suivantes :
                "a*n+b"
                "a*n**2+b*n+c"
                "a*b**n+c"

        """

        self.isInhom = True
        n_index = 0
        solution = "(" + solution + ")"
        self.solut_part = str(solution)

        n = sympy.symbols("n", real=True)
        equation = sympy.Add(0)
        self.coef_recurrence.reverse()  # On commence du coefficient basé sur la puisssance la plus basse du polynôme, pour finir sur celle la plus haute
        for coef in self.coef_recurrence:
            n_part = solution.replace("n", "(n+" + str(n_index) + ")")  # pour chaque indice, on adapte le n afin de l'intégrer dans l'expression
            n_part = parse_expr(n_part, transformations=(standard_transformations + (auto_number,)))  # On parse le string de manière à avoir une expression sympy
            print("terme n+" + str(n_index), " : ", +n_part)
            equation = equation + coef * n_part  # à l'équation on rajoute le terme n+i multiplié par son coefficient
            n_index += 1
        self.coef_recurrence.reverse()  # On remet les coefficient dans l'ordre initial

        print("partie inhomogène : ", equation)
        print("partie inhomogène simplifiée : ", sympy.simplify(equation))
        self.inhom = sympy.simplify(equation)

    def update_coefs(self, coefs):
        """ Mets à jours les différents coefficient (a, b, c, ...) de l'équation

        self.coefs_abc : correspond aux différents coefficients

        Parameters
        ----------
        coefs : list
            liste de longueur égale au nombre de racines de l'équation homogène, contenant les différents coefficients

        Returns
        -------
        True si la liste est de bonne taille et les coefficients ont bien été lus, False sinon

        Raises
        ------
        CoefInputError (todo)
            Si on ne parvient pas à lire les coefficients
        """

        try:  # todo Simplifier cette expression inutilement longue
            if self.isComplex:
                if len(coefs) != len(self.real_roots) + 2 * len(self.complex_roots):
                    print("Number of coefficient not matching")
                    return False
                else:
                    coefs = list(map(lambda r: formatNumber(float(r)), coefs))
                    self.coefs_abc = coefs
                    return True
            else:
                if len(coefs) != len(self.real_roots):
                    print("Number of coefficient not matching")
                    return False
                else:
                    coefs = list(map(lambda r: formatNumber(float(r)), coefs))
                    self.coefs_abc = coefs
                    return True
        except:
            print("Could not read coefficient values")
            return False

    def generate_symbolic_poly(self):
        """
        Génère les expressions sympy correspondant aux expressions factorisées et non-factorisées du polynôme caractéristique

        Il est nécessaire de définir le degré et les racines avant l'exécution de cette fonction
        Cette étape est identique pour les équation homogènes et inhomogènes

        self.equations_symbolic_ref["polyfacto"] devient l'expression sympy du polynôme factorisé
        self.equations_symbolic_ref["polynonfacto"] devient l'expression sympy du polynôme non-factorisé
        self.coef_recurrence devient les coefficients de chaque membre du polynôme non-factorisé (a,b,c,d dans ...an³+bn²+cn+d)

        Returns
        -------
        True si la génération des expressions sympy a bien été réalisée, False sinon

        """
        if self.degree == 0:
            print("Degree = 0, nothing to display")
            return False

        equation = sympy.Add(1)

        if self.isComplex:  # Si l'équation est complexe, cela implique un traitement différents des racines
            x = sympy.symbols("x", real=True)
            for module, argument in self.complex_roots:
                argument = Rational(argument[0], argument[1])
                equation = equation * (x - (module * sympy.cos(argument * sympy.pi) + sympy.I * module * sympy.sin(
                    argument * sympy.pi)))
                equation = equation * (x - (module * sympy.cos(argument * sympy.pi) - sympy.I * module * sympy.sin(
                    argument * sympy.pi)))
            for root in self.real_roots:
                equation = equation * (x - root)

            print("Polynôme factorisé (symbolic) : ", equation)
            self.equations_symbolic_ref["polyfacto"] = equation

            equation_nonfacto = sympy.expand(equation)
            print("Polynôme non-factorisé (symbolic) : ", equation_nonfacto)
            self.equations_symbolic_ref["polynonfacto"] = equation_nonfacto

            self.coef_recurrence = equation_nonfacto.as_poly(gens=x).all_coeffs()
            print("Coefficients du polynôme : ", self.coef_recurrence)
            return True

        else:
            x = sympy.symbols("x", real=True)
            for root in self.real_roots:
                equation = equation * (x - root)
            print("Polynôme factorisé (symbolic) : ", equation)
            self.equations_symbolic_ref["polyfacto"] = equation

            equation_nonfacto = sympy.expand(equation)
            print("Polynôme non-factorisé (symbolic) : ", equation_nonfacto)
            self.equations_symbolic_ref["polynonfacto"] = equation_nonfacto

            self.coef_recurrence = equation_nonfacto.as_poly(gens=x).all_coeffs()
            print("Coefficients du polynôme : ", self.coef_recurrence)
            return True

    def generate_latex_poly(self):
        """
        Génère les expressions latex correspondant aux expressions factorisées et non-factorisées du polynôme caractéristique


        Il est nécessaire de définir les expressions sympy et les coefficients de la solution générale
        Si l'équation est inhomogène, il faut également définir les racines particulières avant

        self.equations_latex_ref["polyfacto"] devient l'expression latex du polynôme factorisé
        self.equations_latex_ref["polynonfacto"] devient l'expression latex du polynôme non-factorisé
        self.equations_latex_ref["recurrence"] devient l'expression latex de l'équation de récurrence sans sa forme U_n
        self.equations_latex_ref["resolution"] devient l'expression latex de la solution générale

        Pour chacune des expressions latex, un png est généré

        Todo gérer les exceptions
        """
        # Polynôme factorisé
        polyfacto = r"$" + sympy.latex(self.equations_symbolic_ref["polyfacto"]) + "$"
        print("Polynôme factorisé (latex) : ", polyfacto)
        eq_to_png(polyfacto, "./latex_tools/polynome_factorisé.png")
        self.equations_latex_ref["polyfacto"] = polyfacto

        # Polynôme non-factorisé
        polynonfacto = r"$" + sympy.latex(self.equations_symbolic_ref["polynonfacto"]) + "$"
        print("Polynôme non-factorisé (latex) : ", polynonfacto)
        eq_to_png(polynonfacto, "latex_tools/polynome_non_factorisé.png")
        self.equations_latex_ref["polynonfacto"] = polynonfacto

        # Equation de récurrence
        recurrence = r""
        un_index = len(self.coef_recurrence) - 1  # On commence par le membre du plus bas degré du polynôme

        for r in self.coef_recurrence:  # Le premier membre de l'expression n'aura jamais de coefficient
            if un_index == 0:
                u_n = "u_{n}"
            else:
                u_n = "u_{n+" + str(un_index) + "}"
            un_index -= 1

            # Pour chaque membre du polynôme, on regarde son coefficient, et on le simplifie si nécessaire, et on ajuste l'expression pour qu'elle soit plus intuitivement lisible
            # en format latex
            if r == 0:
                pass
            elif r == 1:
                recurrence += "+" + u_n
            elif r == -1:
                recurrence += "-" + u_n
            elif r < 0:
                value = str(sympy.Abs(r)).replace("sqrt", "\\sqrt").replace("(", "{").replace(")", "}")
                if ("+" in value) or ("-" in value):
                    recurrence += "-(" + value + ")" + u_n
                else:
                    recurrence += "-" + value + u_n

            else:
                value = str(sympy.Abs(r)).replace("sqrt", "\\sqrt").replace("(", "{").replace(")", "}")
                if ("+" in value) or ("-" in value):
                    recurrence += "+(" + value + ")" + u_n
                else:
                    recurrence += "+" + value + u_n

        # Rajout de la partie inhomogène si besoin
        self.inhom_str = str(self.inhom).replace("**", "^").replace("*", ".").replace("(", "{").replace(")", "}")
        if "/" in self.inhom_str:
            self.inhom_str = "\\frac{" + self.inhom.replace("/", "}{") + "}"
        recurrence = r"$" + recurrence[1:] + "=" + self.inhom_str + "$"

        eq_to_png(recurrence, "latex_tools/équation_de_récurrence.png")
        highlight("latex_tools/équation_de_récurrence.png", "latex_tools/équation_de_récurrence_highlight.png")
        print("équation de récurrence (latex) :", recurrence)
        self.equations_latex_ref["recurrence"] = recurrence

        # Solution générale
        resolution = r""
        index = 0
        for i in range(len(self.real_roots)):
            r = self.real_roots[i]
            racine_multiple = 0
            for j in range(i + 1, len(self.real_roots)):  # On vérifie si c'est une racine multiple, pour l'adapter en fonction
                if self.real_roots[j] == r:
                    racine_multiple += 1
            if racine_multiple == 1:
                if r < 0:
                    resolution += "+" + alphabet[index] + "n(" + str(r) + ")^n"
                else:
                    resolution += "+" + alphabet[index] + "n" + str(r) + "^n"
            elif racine_multiple > 1:
                if r < 0:
                    resolution += "+" + alphabet[index] + "n^" + str(racine_multiple) + "(" + str(r) + ")^n"
                else:
                    resolution += "+" + alphabet[index] + "n^" + str(racine_multiple) + str(r) + "^n"
            else:
                if r < 0:
                    resolution += "+" + alphabet[index] + "(" + str(r) + ")^n"
                else:
                    resolution += "+" + alphabet[index] + str(r) + "^n"
            index += 1

        if self.isComplex == True:
            for r in self.complex_roots:
                module, argument = r
                resolution += "+" + alphabet[index] + str(module) + "^n" + "\\cos n" + "\\frac{" + str(
                    argument[0]) + "\pi}{" + str(argument[1]) + "}"
                index += 1
                resolution += "+" + alphabet[index] + str(module) + "^n" + "\\sin n" + "\\frac{" + str(
                    argument[0]) + "\pi}{" + str(argument[1]) + "}"
                index += 1

        if self.isInhom:
            resolution = r"$U_n=" + resolution[1:] + "+" + self.solut_part.replace("**", "^").replace("*",
                                                                                                      ".") + "$"
        else:

            resolution = r"$U_n=" + resolution[1:] + "$"
        eq_to_png(resolution, "latex_tools/résolution.png")
        highlight("latex_tools/résolution.png", "latex_tools/résolution_highlight.png")
        print("résolution (latex) :", recurrence)
        self.equations_latex_ref["recurrence"] = recurrence
        self.equations_latex_ref["resolution"] = resolution

    def generate_solution(self):
        """
        Calcule les contraintes à partir de la solution générale pour les différentes valeurs de n (0,1,2,... en fonction du degré)


        Il est nécessaire de définir les expressions sympy et les coefficients de la solution générale
        Si l'équation est inhomogène, il faut également définir les racines particulières avant

        self.equations_latex_ref["un_values"] devient l'expression principale du système d'équations de récurrence dans sa forme Un
        self.equations_latex_ref["contraintes"] devient l'expression latex des différentes contraintes sur le système pour les différentes valeurs de n
        un png des contraintes est généré

        Todo cette fonction peut éventuellement être intégrée dans generate_latex_poly
        Todo gérer les exceptions
        """
        un_values = []
        for i in range(self.degree):
            un_value = 0
            index = 0
            if self.isComplex == False:
                for j in range(len(self.real_roots)):
                    r = self.real_roots[i]
                    racine_multiple = 0
                    for k in range(j + 1, len(self.real_roots)):
                        if self.real_roots[k] == r:
                            racine_multiple += 1
                    un_value += self.coefs_abc[index] * (i ** racine_multiple) * (r ** i)
                    index += 1
            else:
                un_value = ""
                for r in self.real_roots:
                    un_value += str(formatNumber(self.coefs_abc[index] * (r ** i))) + "+"
                    index += 1

                for r in self.complex_roots:
                    module, argument = r
                    """ A cause des racines, il y a souvent des cas où on est très proches des entiers, j'avais prévu quelque chose pour rendre plus lisible les expressions,
                        mais j'ai préféré mettre ça de côté pour le moment
                        
                    if False and isInteger(math.cos(i * argument[0] * math.pi / argument[1]) % 1):
                        un_value += str(formatNumber(self.coefs_abc[index] * (module ** i) * round( 
                            math.cos(i * argument[0] * math.pi / argument[1])))) + "+"
                        index += 1
                        un_value += str(formatNumber(self.coefs_abc[index] * (module ** i) * round(
                            math.sin(i * argument[0] * math.pi / argument[1])))) + "+"
                        index += 1
                    else:
                    """

                    un_value += str(
                        formatNumber(self.coefs_abc[index] * module ** i)) + ".\\cos{(\\frac{" + str(
                        i * argument[0]) + "}{" + str(argument[1]) + "}\\pi)}+"
                    # un_value+=self.coefs_abc[index]*(module**i)*(math.cos(i*argument[0]*math.pi/argument[1]))
                    index += 1
                    # un_value+=self.coefs_abc[index]*(module**i)*(math.sin(i*argument[0]*math.pi/argument[1]))
                    un_value += str(
                        formatNumber(self.coefs_abc[index] * module ** i)) + ".\\sin{(\\frac{" + str(
                        i * argument[0]) + "\\pi}{" + str(argument[1]) + "})}+"
                    index += 1
                un_value = un_value[:-1]
            if self.isInhom:
                inhom_value = self.solut_part
                inhom_value = inhom_value.replace('n', str(i))
                inhom_value = parse_expr(inhom_value, transformations=(standard_transformations + (auto_number,)))
                un_value += float(inhom_value)

            if not self.isComplex:
                un_value = str(formatNumber(un_value))
                un_values.append(r"$u_" + str(i) + "=" + un_value + "$")
            else:
                un_values.append(r"$u_" + str(i) + "=" + un_value + "$")

        self.equations_latex_ref["un_values"] = un_values
        print("Contraintes (latex) :", un_values)

        un_latex = r""
        contraintes_latex = ""
        for un in un_values:
            un_latex += un + "\n"
            contraintes_latex += un[1:-1] + "\\\ \n"
        contraintes_latex = contraintes_latex[:-4]
        self.equations_latex_ref["contraintes"] = contraintes_latex
        un_latex = un_latex[:-1]

        eq_to_png(un_latex, "latex_tools/contraintes.png")

    def generate_latex_file(self):
        """
        Génère un fichier latex sur base de l'équation

        En fonction que l'équation soit complèxe ou inhomogène, le format du fichier peut être différent

        Todo gérer les exceptions
        """

        # Le fichier est généré bloc par bloc, avec un bloc correspondant au début du fichier, un à la question, un la résolution, et un à la fin
        # Le bloc du début et de la fin sont communs à toutes les équations
        # Todo la génération est inutilement complèxe et longue, il y a moyen de simplifier tout ça
        if not self.isComplex:
            file_content = generate_start() + generate_question(self.equations_latex_ref["recurrence"][1:-1],
                                                                self.equations_latex_ref["contraintes"])
            if not self.isInhom:
                file_content += generate_solution(self.real_roots, self.isInhom,
                                                  self.equations_latex_ref["resolution"][1:-1], self.coefs_abc,
                                                  solution_particuliere="")
            else:
                file_content += generate_solution(self.real_roots, self.isInhom,
                                                  self.equations_latex_ref["resolution"][1:-1], self.coefs_abc,
                                                  solution_particuliere=self.solut_part[1:-1].replace("**",
                                                                                                      "^").replace("*",
                                                                                                                   "."))

            file_content += generate_end()

            with open("./recursion.tex", "w") as f:
                f.write(file_content)
        else:
            file_content = generate_start() + generate_question(self.equations_latex_ref["recurrence"][1:-1],
                                                                self.equations_latex_ref["contraintes"])
            file_content += generate_solution_complex(self.real_roots, self.complex_roots, self.isInhom,
                                                      self.equations_latex_ref["resolution"][1:-1], self.coefs_abc,
                                                      solution_particuliere="")
            file_content += generate_end()
            with open("./recursion.tex", "w") as f:
                f.write(file_content)
