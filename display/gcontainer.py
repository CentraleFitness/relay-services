from display.container import Container

from PIL import Image

class GContainer(Container):
    """Short for 'Graphic Container'"""

    def __init__(self):
        super().__init__()

    def translate(self) -> Image:
        return Image.new('1', (128, 64), color=0)
