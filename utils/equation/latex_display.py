import matplotlib.pyplot as plt
from PIL import Image

def eq_to_png(eq,file):
    """
    Génère une image correspondant à une expression latex

    Parameters
    ----------
    eq : str
        expression Latex à transformer en png
    file : str
        destination du fichier .png
    """
    fig = plt.figure(figsize=(0.01, 0.01))
    ax = fig.add_subplot(111)
    ax.text(0, 0, eq, fontsize=12)
    plt.axis('off')
    plt.savefig(file, transparent=True, dpi=300, bbox_inches='tight', pad_inches=0.02)


def highlight(equation,new_equation):
    """
    Modifie une image de manière à l'encadrer

    Parameters
    ----------
    eq : str
        source du fichier .png à transformer
    file : str
        destination du nouveau fichier .png
    """
    equation_image = Image.open(equation).convert("RGBA")
    background = Image.open("resources/equation highlight.png").convert("RGBA")
    equation_highlight = Image.new("RGBA", size=(equation_image.width + 30, equation_image.height + 30))
    background = background.resize(equation_highlight.size)
    equation_highlight.paste(background, (0, 0), background)
    equation_highlight.paste(equation_image, (15, 15), equation_image)
    equation_highlight.save(new_equation)
