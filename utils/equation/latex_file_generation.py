def generate_start():
    packages = "\\documentclass[12pt]{article}\n\\usepackage[utf8]{inputenc}\n\\usepackage{amsmath}\n\\usepackage{amssymb}\n"
    startdocument = "\\begin{document}\n"
    return packages+startdocument

def generate_question(equation,contraintes):
    enonce = "R\\'esoudre le syst\\`eme d'\\'equations de r\\'ecurrence suivant d\\'efini pour $n \in \mathbb{N}$:\n"
    start = "\\begin{align*}\n\\left\\{\\begin{array}{l}\n"
    end ="\\end{array}\n\\right.\n\\end{align*}\n\n"
    return enonce+start+equation+"\\\ \n"+contraintes+"\n"+end

def generate_solution(racines,is_inhom,solution,contraintes,solution_particuliere=""):
    solutionstart = "\n\n\n\n%--------- SOLUTION ---------\n%\\begin{solution}\n\\vspace{3cm}"
    racinestex = "Les racines de l'\\'equation caract\\'eristique sont "
    for i in racines[0:-1]:
        racinestex += "$"+str(i)+"$, "
    racinestex=racinestex[:-2]
    racinestex+= " et $"+str(racines[-1])+"$"
    if is_inhom:
        solut_part = ", et une solution particuli\\`ere est :\n"

        solut_part += "\\begin{align*}\n"
        solut_part += solution_particuliere
        solut_part += "\n\\end{align*}\n"
    else:
        solut_part = ""
        racinestex += ".\\\ \n"

    reso = "\nLa solution g\\'en\\'erale est\n"
    reso += "\\begin{align*}\n"
    reso += solution
    reso += "\n\\end{align*}\n\n"
    reso+= "\no\\`u "

    contraintestex=""
    alphab = [chr(i) for i in range(ord('a'), ord('z') + 1)]
    for i in range(len(contraintes)-1):
        contraintestex += "$"+alphab[i]+" = "+str(contraintes[i])+"$, "
    contraintestex=contraintestex[:-2]
    contraintestex+= " et $"+alphab[i+1]+" = "+str(contraintes[i+1])+"$.\n\n"

    return solutionstart+racinestex+solut_part+reso+contraintestex

def generate_solution_complex(racines,racines_complexes,is_inhom,solution,contraintes,solution_particuliere=""):
    if len(racines_complexes)==0:
        return generate_solution(racines,is_inhom,solution,contraintes,solution_particuliere)

    solutionstart = "\n\n\n\n%--------- SOLUTION ---------\n%\\begin{solution}\n\\vspace{3cm}"
    racinestex = "Les racines de l'\\'equation caract\\'eristique sont "
    for i in racines:
        racinestex += "$"+str(i)+"$, "
    for r in racines_complexes[0:-1]:
        module, argument = r
        racinestex += "$"+str(module)+"\\cos("+"\\frac{"+str(argument[0])+"\pi}{"+str(argument[1])+"})+"+\
                      str(module)+"\\sin("+"\\frac{"+str(argument[0])+"\pi}{"+str(argument[1])+"})i$, "
        racinestex += "$"+str(module)+"\\cos("+"\\frac{"+str(argument[0])+"\pi}{"+str(argument[1])+"})-"+\
                      str(module)+"\\sin("+"\\frac{"+str(argument[0])+"\pi}{"+str(argument[1])+"})i$, "
    module,argument=racines_complexes[-1]
    racinestex+= "$"+str(module)+"\\cos("+"\\frac{"+str(argument[0])+"\pi}{"+str(argument[1])+"})+"+\
                      str(module)+"\\sin("+"\\frac{"+str(argument[0])+"\pi}{"+str(argument[1])+"})i$ et "
    racinestex += "$"+str(module)+"\\cos("+"\\frac{"+str(argument[0])+"\pi}{"+str(argument[1])+"})-"+\
                  str(module)+"\\sin("+"\\frac{"+str(argument[0])+"\pi}{"+str(argument[1])+"})i$"



    if is_inhom:
        solut_part = ", et une solution particuli\\`ere est :\n"

        solut_part += "\\begin{align*}\n"
        solut_part += solution_particuliere
        solut_part += "\n\\end{align*}\n"
    else:
        solut_part = ""
        racinestex += ".\\\ \n"

    reso = "\nLa solution g\\'en\\'erale est\n"
    reso += "\\begin{align*}\n"
    reso += solution
    reso += "\n\\end{align*}\n\n"
    reso+= "\no\\`u "

    contraintestex=""
    alphab = [chr(i) for i in range(ord('a'), ord('z') + 1)]
    for i in range(len(contraintes)-1):
        contraintestex += "$"+alphab[i]+" = "+str(contraintes[i])+"$, "
    contraintestex=contraintestex[:-2]
    contraintestex+= " et $"+alphab[i+1]+" = "+str(contraintes[i+1])+"$.\n\n"

    return solutionstart+racinestex+solut_part+reso+contraintestex


def generate_end():
    enddocument = "\\end{document}"
    return enddocument
