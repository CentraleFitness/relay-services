from .cursor import Cursor
from .iterator import Iterator

class Container(object):
    """Contrain"""
    
    def __init__(self, *args, **kwargs):
        self.objects = kwargs.get('objects', list())
        assert isinstance(self.objects, list)
        self.cursor = Iterator(self.objects)
        self.parent = kwargs.get('parent', None)

    def reset_iterator(self):
        self.cursor = Iterator(self.objects)

