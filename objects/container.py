from .cursor import Cursor
from .iterator import Iterator

class Container(object):
    """Contrain"""
    
    def __init__(self, *args, **kwargs):
        self.objects = kwargs.get('objects', list())
        assert isinstance(self.objects, list)
        self.parent = kwargs.get('parent', None)
        self.cursor = Iterator(self.objects)
        self.actions = dict()
        self.actions['U'] = (self.cursor.prev, None)
        self.actions['D'] = (self.cursor.next, None)

    def reset_iterator(self):
        self.cursor = Iterator(self.objects)

    def interact(self, input: str) -> None:
        if input in self.actions:
            return self.actions[input]
        return self.cursor().action(input)
