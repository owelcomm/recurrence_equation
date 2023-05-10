def generate_start():
    """ Génère le début d'un document latex

        Returns
        -------
        packages+startdocument, str
            packages correspond à l'ensemble des packages devant être inclu dans le fichier latex
            startdocument correpond à l'entête du document latex
        """
    packages = "\\documentclass[12pt]{article}\n\\usepackage[utf8]{inputenc}\n\\usepackage{amsmath}\n\\usepackage{amssymb}\n"
    startdocument = "\\begin{document}\n"
    return packages+startdocument

def generate_question(equation,contraintes):
    """ Génère la question à poser dans le document latex

    Parameters
    ----------
    equation : str
        le format latex de l'équation principale du système d'équations de récurrence

    contraintes : str
        le format latex des contraintes imposées sur le système d'équations

    Returns
    -------
    str
        la section latex du document correspondant à la question posée

    """
    enonce = "R\\'esoudre le syst\\`eme d'\\'equations de r\\'ecurrence suivant d\\'efini pour $n \in \mathbb{N}$:\n"
    start = "\\begin{align*}\n\\left\\{\\begin{array}{l}\n"
    end ="\\end{array}\n\\right.\n\\end{align*}\n\n"
    return enonce+start+equation+"\\\ \n"+contraintes+"\n"+end

def generate_solution(racines,is_inhom,solution,contraintes,solution_particuliere=""):

    """ Génère la résolution du système d'équations de récurrence en latex, pour les équations non-complèxes

    Parameters
    ----------
    racines : list
        liste des racines de l'équation (float)

    is_inhom: bool
        True si l'équation est inhomogène, False sinon

    solution: str
        Solution générale de l'équation en format latex

    contraintes: list
        liste des coefficients a,b,c,... de la solution générale de l'équation (float)

    solution_particuliere, str, opt
        solution particulière en format latex


    Returns
    -------
    str
        La section du fichier latex correspondant à la résolution de la question

    """
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
    """ Génère la résolution du système d'équations de récurrence en latex, pour les équations complèxes

    Parameters
    ----------
    racines : list
        liste des racines réelles de l'équation (float)

    racines_complexes : list
            les racines sont de la forme suivante :
                root : tuple (module,argument)
                module : float
                argument : tuple (int,int) correspondant respectivement au numérateur et dénumérateur multipliant pi
                            par exemple, un argument de 3π/4 correspondra à (3,4). Ce choix a été fait, par rapport à un
                            float, afin de représenter de manière plus intuitive la fraction lors de la génération du
                            fichier latex

    is_inhom: bool
        True si l'équation est inhomogène, False sinon

    solution: str
        Solution générale de l'équation en format latex

    contraintes: list
        liste des coefficients a,b,c,... de la solution générale de l'équation (float)

    solution_particuliere, str, opt
        solution particulière en format latex


    Returns
    -------
    str
        La section du fichier latex correspondant à la résolution de la question

    """
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
    """ Génère la fin d'un document latex

        Returns
        -------
        enddocument, str
            fin du document latex
        """
    enddocument = "\\end{document}"
    return enddocument
