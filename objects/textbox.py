class TextBox(object):
    """TextBox"""
    def __init__(self, txt = ""):
        assert isinstance(txt, str, int)
        self.text = str(txt) if isinstance(txt, int) else txt
        pass
