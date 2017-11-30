from .cursor import Cursor

class Container(object):
    """Contrain"""
    
    def __init__(self, *args, **kwargs):
        self.objects = kwargs.get('objects', list())
        assert isinstance(self.objects, list)
        self.cursor = Cursor(len(self.objects), True)
        self.parent = kwargs.get('parent', None)

    def interact(self):
        # TODO
        # self.objects[self.cursor.curr].interact()
        pass
