
class Container(object):
    """Contrain"""
    
    def __init__(self, *args, **kwargs):
        self.objects = kwargs.get('objects', list())
        assert isinstance(self.objects, list)
