import pylab
from PIL import Image

def eq_to_png(eq,file):
    fig = pylab.figure(figsize=(0.01, 0.01))
    ax = fig.add_subplot(111)
    ax.text(0, 0, eq, fontsize=12)
    pylab.axis('off')
    pylab.savefig(file, transparent=True, dpi=300, bbox_inches='tight', pad_inches=0.02)


def highlight(equation,new_equation):
    equation_image = Image.open(equation).convert("RGBA")
    background = Image.open("resources/equation highlight.png").convert("RGBA")
    equation_highlight = Image.new("RGBA", size=(equation_image.width + 30, equation_image.height + 30))
    background = background.resize(equation_highlight.size)
    equation_highlight.paste(background, (0, 0), background)
    equation_highlight.paste(equation_image, (15, 15), equation_image)
    equation_highlight.save(new_equation)
