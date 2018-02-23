from collections import defaultdict

from .iterator import Iterator

class Container(object):
    """Contrain"""

    def __init__(self, *args, **kwargs):
        self.objects = kwargs.get('objects', list())
        assert isinstance(self.objects, list)
        self.parent = kwargs.get('parent', None)
        self.iter = Iterator(self.objects)
        self.actions = defaultdict()
        self.actions['U'] = (self.iter.prev, None)
        self.actions['D'] = (self.iter.next, None)

    def reset_iterator(self):
        self.iter = Iterator(self.objects)

    def interact(self, input: str) -> None:
        if input in self.actions:
            return self.actions[input]
        return self.iter().action[input]
