from PIL import Image, ImageFont, ImageDraw, ImageOps
from collections import defaultdict

from objects.textbox import TextBox


class GTextBox(TextBox):
    """description of class"""

    def __init__(self, size: tuple, pos: tuple, *args, **kwargs):
        """
        size: a tuple containing the size (x, y) of the object
        position: a tuple containing the distance (x, y)
                  from the top-left corner of the parent container
        kwargs:
            font: The font to use, 'None' to use the default font
            x: x offset
            y: y offset
            action: tuple as (function, (params, ))
        """
        self.gsize = size
        self.gpos = pos

        fontname = kwargs.get('font', None)
        self.gfont = ImageFont.truetype(fontname)   \
            if fontname else ImageFont.load_default()
        self.gx = kwargs.get('x', 0)
        self.gy = kwargs.get('y', 0)
        self.action = kwargs.get('action', defaultdict(tuple))
        self.goto = None
        return super().__init__(*args, **kwargs)

    def action_on_click(self) -> tuple:
        return self.action

    def translate(self, *args, **kwargs):
        render = Image.new('1', self.gsize, 0)
        draw = ImageDraw.Draw(render)
        draw.text((self.gx, self.gy), self.text, 1, self.gfont)
        if kwargs.get('selected', False):
            render = render.convert('L')
            render = ImageOps.invert(render)
            render = render.convert('1')
        return render, self.gpos
