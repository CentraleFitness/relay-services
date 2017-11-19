class Scrollbar(object):
    """ScrollBar"""
    def __init__(self, nb_pages: int, current: int = 1):
        self.nb_pages = nb_pages
        self.current = current
        assert nb_pages > 0 and current > 0 and current <= nb_pages
