from PIL import Image

from objects.container import Container
from objects.button import Button
from objects.label import Label
from objects.scrollbar import ScrollBar
from objects.textbox import TextBox

class GContainer(Container):
    """Short for 'Graphic Container'"""

    def __init__(self):
        super().__init__()

    def translate(self) -> Image:
        render = Image.new('1', (128, 64), color=0)
        for obj in self.objects:
            if isinstance(obj, Label):
                pass
            elif isinstance(obj, TextBox):
                pass
            elif isinstance(obj, Button):
                pass
            elif isinstance(obj, ScrollBar):
                pass
        return render
