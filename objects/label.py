class Label(object):
    """
    Label: contrary to the TextBox, the content should not be modified
    after being instanciated
    """

    def __init__(self, txt = ""):
        assert isinstance(txt, str, int)
        self.text = str(txt) if isinstance(txt, int) else txt
