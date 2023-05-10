import sympy
from sympy import Rational
import math
from utils.equation.latex_display import eq_to_png, highlight
from sympy.parsing.sympy_parser import parse_expr,standard_transformations, auto_number
import random as rd

from utils.equation.latex_file_generation import generate_start, generate_question, generate_solution, generate_end, \
    generate_solution_complex

alphabet = [chr(i) for i in range(ord('a'), ord('z') + 1)]
alphabet_maj = [chr(i) for i in range(ord('A'), ord('Z') + 1)]
formatNumber = lambda n: n if n % 1 else int(n)

def isInteger(x):
    if abs(x%1)<=0.00001 or abs(x%1-1)<=0.00001:
        return True
    else:
        return False

class Equation:
    def __init__(self, isComplex=False, degree=0, real_roots=[], complex_roots=[]):
        self.isComplex = isComplex
        self.degree = degree
        self.real_roots = real_roots
        self.complex_roots = complex_roots
        self.equations_symbolic_ref = {}
        self.equations_latex_ref = {}
        self.coef_recurrence = []
        self.coefs_abc = []
        self.inhom="0"
        self.isInhom=False

    def update_degree(self, degree):
        try:
            self.degree = int(degree)
            return True
        except:
            print("Could not read degree value")
            return False

    def update_real_roots(self, roots):
        try:
            roots = list(map(lambda r: float(r), roots))
            self.real_roots = roots
            return True
        except:
            print("Could not read real roots values")
            return False

    def add_complex_roots(self, root):
        print(self.complex_roots)
        self.complex_roots.append(root)

    def generate_solut_part(self):
        values=list(range(-5,-1))+list(range(2,6))
        signvalues=['-'+str(abs(i)) if i<0 else '+'+str(abs(i)) for i in values]
        type = rd.randint(1,5)
        print("type d'équation : ", type)
        if type==1 or type==2 : #an+b
            a_value=rd.choice(values)
            b_value=rd.choice(signvalues)
            eq = str(a_value)+"*n"+b_value
        elif type==3 or type==4: #an²+bn+c
            a_value=rd.choice(values)
            b_value=rd.choice(signvalues)
            c_value=rd.choice(signvalues)
            eq = str(a_value)+"*n**2"+b_value+"*n"+c_value
        elif type==5: #ab^(n)+c
            a_value=rd.choice(values)
            b_value=abs(rd.choice(values))
            c_value=rd.choice(signvalues)
            eq = str(a_value)+"*"+str(b_value)+"**n"+c_value
        print("solution particulière : ", eq)
        return eq


    def add_solut_part(self, solution):
        self.isInhom=True
        n_index=0
        solution = "("+solution+")"
        self.solut_part = str(solution)
        n = sympy.symbols("n", real=True)

        equation = sympy.Add(0)
        self.coef_recurrence.reverse()
        for coef in self.coef_recurrence:
            n_part = solution.replace("n","(n+"+str(n_index)+")")
            n_part = parse_expr(n_part, transformations=(standard_transformations + (auto_number,)))
            print("terme n+"+str(n_index)," : ",+n_part)
            equation=equation+coef*n_part
            n_index+=1
        self.coef_recurrence.reverse()

        print("partie inhomogène : ", equation)
        print("partie inhomogène simplifiée : ", sympy.simplify(equation))
        self.inhom=sympy.simplify(equation)


    def update_coefs(self, coefs):
        try:
            if self.isComplex:
                if len(coefs)!=len(self.real_roots)+2*len(self.complex_roots):
                    print("Number of coefficient not matching")
                    return False
                else:
                    coefs = list(map(lambda r: formatNumber(float(r)), coefs))
                    self.coefs_abc = coefs
                    return True
            else:
                if len(coefs)!=len(self.real_roots):
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
        if self.degree == 0:
            print("Degree = 0, nothing to display")
            return False

        equation = sympy.Add(1)
        if self.isComplex:
            x = sympy.symbols("x", real=True)
            for module, argument in self.complex_roots:
                argument = Rational(argument[0], argument[1])
                equation = equation * (x - (module*sympy.cos(argument*sympy.pi) + sympy.I*module*sympy.sin(argument*sympy.pi)))
                equation = equation * (x - (module*sympy.cos(argument*sympy.pi) - sympy.I*module*sympy.sin(argument*sympy.pi)))
            for root in self.real_roots:
                equation = equation * (x - root)

            print("Polynôme factorisé (symbolic) : ", equation)
            self.equations_symbolic_ref["polyfacto"] = equation

            equation_nonfacto = sympy.expand(equation)
            print("Polynôme non-factorisé (symbolic) : ", equation_nonfacto)
            self.equations_symbolic_ref["polynonfacto"] = equation_nonfacto

            self.coef_recurrence = equation_nonfacto.as_poly(gens=x).all_coeffs()
            print("Coefficients du polynôme : ",self.coef_recurrence)
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
            print("Coefficients du polynôme : ",self.coef_recurrence)
            return True

    def generate_latex_poly(self):
        if False:
            pass

        else:
            #Polynômes
            polyfacto = r"$"+sympy.latex(self.equations_symbolic_ref["polyfacto"])+"$"
            print("Polynôme factorisé (latex) : ", polyfacto)
            eq_to_png(polyfacto,"./latex_tools/polynome_factorisé.png")
            self.equations_latex_ref["polyfacto"]=polyfacto

            polynonfacto = r"$"+sympy.latex(self.equations_symbolic_ref["polynonfacto"])+"$"
            print("Polynôme non-factorisé (latex) : ", polynonfacto)
            eq_to_png(polynonfacto,"latex_tools/polynome_non_factorisé.png")
            self.equations_latex_ref["polynonfacto"]=polynonfacto

            #Equation de récurrence
            recurrence = r""
            un_index=len(self.coef_recurrence)-1
            for r in self.coef_recurrence:
                if un_index==0:
                    u_n = "u_{n}"
                else:
                    u_n = "u_{n+"+str(un_index)+"}"
                un_index-=1

                #Adjust written coefficient accordingly
                if r==0:
                    pass
                elif r==1:
                    recurrence+="+"+u_n
                elif r==-1:
                    recurrence+="-"+u_n
                elif r<0 :
                    value = str(sympy.Abs(r)).replace("sqrt","\\sqrt").replace("(","{").replace(")","}")
                    if ("+" in value) or ("-" in value):
                        recurrence+="-("+value+")"+u_n
                    else:
                        recurrence+="-"+value+u_n

                else :
                    value = str(sympy.Abs(r)).replace("sqrt","\\sqrt").replace("(","{").replace(")","}")
                    if ("+" in value) or ("-" in value):
                        recurrence+="+("+value+")"+u_n
                    else:
                        recurrence+="+"+value+u_n


            #Rajout de la partie inhomogène si besoin
            self.inhom_str = str(self.inhom).replace("**","^").replace("*",".").replace("(","{").replace(")","}")
            if "/" in self.inhom_str:
                self.inhom_str="\\frac{"+self.inhom.replace("/","}{")+"}"
            recurrence = r"$"+recurrence[1:]+"="+self.inhom_str+"$"


            eq_to_png(recurrence,"latex_tools/équation_de_récurrence.png")
            highlight("latex_tools/équation_de_récurrence.png","latex_tools/équation_de_récurrence_highlight.png")
            print("équation de récurrence (latex) :", recurrence)
            self.equations_latex_ref["recurrence"]=recurrence

            #Résolution
            resolution = r""
            index=0
            for i in range(len(self.real_roots)):
                r= self.real_roots[i]
                racine_multiple=0
                for j in range (i+1,len(self.real_roots)):
                    if self.real_roots[j]==r:
                        racine_multiple+=1
                if racine_multiple==1:
                    if r<0:
                        resolution+= "+"+alphabet[index]+"n("+str(r)+")^n"
                    else:
                        resolution+= "+"+alphabet[index]+"n"+str(r)+"^n"
                elif racine_multiple>1:
                    if r<0:
                        resolution+= "+"+alphabet[index]+"n^"+str(racine_multiple)+"("+str(r)+")^n"
                    else:
                        resolution+= "+"+alphabet[index]+"n^"+str(racine_multiple)+str(r)+"^n"
                else:
                    if r<0:
                        resolution+= "+"+alphabet[index]+"("+str(r)+")^n"
                    else:
                        resolution+= "+"+alphabet[index]+str(r)+"^n"
                index+=1

            if self.isComplex==True:
                for r in self.complex_roots:
                    module, argument = r
                    resolution+= "+"+alphabet[index]+str(module)+"^n"+"\\cos n"+"\\frac{"+str(argument[0])+"\pi}{"+str(argument[1])+"}"
                    index+=1
                    resolution+= "+"+alphabet[index]+str(module)+"^n"+"\\sin n"+"\\frac{"+str(argument[0])+"\pi}{"+str(argument[1])+"}"
                    index+=1

            if self.isInhom :
                resolution = r"$U_n="+resolution[1:]+"+"+self.solut_part.replace("**","^").replace("*",".")+"$"
            else:

                resolution = r"$U_n="+resolution[1:]+"$"
            eq_to_png(resolution,"latex_tools/résolution.png")
            highlight("latex_tools/résolution.png","latex_tools/résolution_highlight.png")
            print("résolution (latex) :", recurrence)
            self.equations_latex_ref["recurrence"]=recurrence
            self.equations_latex_ref["resolution"]=resolution


    def generate_solution(self):
        if False:
            pass

        else:
            un_values = []
            for i in range(self.degree):
                un_value=0
                index=0
                if self.isComplex == False:
                    for j in range(len(self.real_roots)):
                        r= self.real_roots[i]
                        racine_multiple=0
                        for k in range (j+1,len(self.real_roots)):
                            if self.real_roots[k]==r:
                                racine_multiple+=1
                        un_value+=self.coefs_abc[index]*(i**racine_multiple)*(r**i)
                        index+=1
                else:
                    un_value=""
                    for r in self.real_roots:
                        un_value+=str(formatNumber(self.coefs_abc[index]*(r**i)))+"+"
                        index+=1

                    for r in self.complex_roots:
                        module, argument = r #Todo mettre dans un format lisible et prendre en compte les valeurs particulières (i = 0, 1, et cos/sin entier)
                        if False and isInteger(math.cos(i*argument[0]*math.pi/argument[1])%1) :
                            un_value += str(formatNumber(self.coefs_abc[index] * (module ** i) * round(math.cos(i * argument[0] * math.pi / argument[1]))))+"+"
                            index+=1
                            un_value += str(formatNumber(self.coefs_abc[index] * (module ** i) * round(math.sin(i * argument[0] * math.pi / argument[1]))))+"+"
                            index += 1
                        else:
                            un_value+=str(formatNumber(self.coefs_abc[index]*module**i))+".\\cos{(\\frac{"+str(i*argument[0])+"}{"+str(argument[1])+"}\\pi)}+"
                            #un_value+=self.coefs_abc[index]*(module**i)*(math.cos(i*argument[0]*math.pi/argument[1]))
                            index+=1
                            #un_value+=self.coefs_abc[index]*(module**i)*(math.sin(i*argument[0]*math.pi/argument[1]))
                            un_value+=str(formatNumber(self.coefs_abc[index]*module**i))+".\\sin{(\\frac{"+str(i*argument[0])+"\\pi}{"+str(argument[1])+"})}+"
                            index+=1
                    un_value=un_value[:-1]
                if self.isInhom:
                    inhom_value = self.solut_part
                    inhom_value=inhom_value.replace('n',str(i))
                    inhom_value= parse_expr(inhom_value, transformations=(standard_transformations + (auto_number,)))
                    un_value+=float(inhom_value)

                if not self.isComplex:
                    un_value=str(formatNumber(un_value))
                    un_values.append(r"$u_"+str(i)+"="+un_value+"$")
                else :
                    un_values.append(r"$u_"+str(i)+"="+un_value+"$")


            self.equations_latex_ref["un_values"]=un_values
            print("Contraintes (latex) :",un_values)

            un_latex = r""
            contraintes_latex = ""
            for un in un_values:
                un_latex+=un+"\n"
                contraintes_latex+=un[1:-1]+"\\\ \n"
            contraintes_latex=contraintes_latex[:-4]
            self.equations_latex_ref["contraintes"] = contraintes_latex
            un_latex=un_latex[:-1]


            eq_to_png(un_latex,"latex_tools/contraintes.png")


    def generate_latex_file(self):
        if not self.isComplex:
            file_content = generate_start()+generate_question(self.equations_latex_ref["recurrence"][1:-1],self.equations_latex_ref["contraintes"])
            if not self.isInhom:
                file_content += generate_solution(self.real_roots,self.isInhom,self.equations_latex_ref["resolution"][1:-1],self.coefs_abc,solution_particuliere="")
            else:
                file_content += generate_solution(self.real_roots,self.isInhom,self.equations_latex_ref["resolution"][1:-1],self.coefs_abc,solution_particuliere=self.solut_part[1:-1].replace("**", "^").replace("*", "."))

            file_content+=generate_end()

            with open("./recursion.tex", "w") as f:
                f.write(file_content)
        else:
            file_content = generate_start()+generate_question(self.equations_latex_ref["recurrence"][1:-1],self.equations_latex_ref["contraintes"])
            file_content += generate_solution_complex(self.real_roots, self.complex_roots, self.isInhom,
                                              self.equations_latex_ref["resolution"][1:-1], self.coefs_abc,
                                              solution_particuliere="")
            file_content += generate_end()
            with open("./recursion.tex", "w") as f:
                f.write(file_content)