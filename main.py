from utils.equation.equation import Equation
from utils.display.main_window import MainApp
from math import sqrt
if __name__ == '__main__':

    MainApp().run()

    #print("exemple équation simple")
    #eq = Equation(degree=3, real_roots=[1,2,3])
    #eq.generate_symbolic_poly()
    #eq.generate_latex_poly()
    #eq.update_coefs([1,2,3])
    #eq.generate_solution()
    #eq.generate_latex_file()
    #
    #print("exemple équation complexe")
    #eq = Equation(degree=3, real_roots=[4], isComplex=True)
    #eq.add_complex_roots((4,(5,4)))
    #eq.generate_symbolic_poly()
    #eq.generate_latex_poly()
    #eq.update_coefs([1, 2, 3])
    #eq.generate_solution()
    #
    #print("\n\n\nexemple équation inhomogène")
    #eq = Equation(degree=3, real_roots=[1,2,3])
    #eq.generate_symbolic_poly()
    #eq.add_solut_part("6*n-3")
    #
    #

    #EXAMEN JANVIER 2020
    # print("\n\n\nexemple équation inhomogène")
    # eq = Equation(degree=2, real_roots=[2,2])
    # eq.generate_symbolic_poly()
    # eq.update_coefs([-3,5/2])
    # eq.add_solut_part("n**2*2**n")
    # eq.generate_latex_poly()
    # eq.generate_solution()
    # eq.generate_latex_file()

    # EXAMEN AOUT 2018
    # print("\n\n\nexemple équation inhomogène")
    # eq = Equation(degree=3, real_roots=[2,2,2])
    # eq.generate_symbolic_poly()
    # eq.update_coefs([-1,3,2])
    # eq.add_solut_part("-2")
    # eq.generate_latex_poly()
    # eq.generate_solution()
    # eq.generate_latex_file()

    pass