class Cursor(object):
    """description of class"""

    def __init__(self, max: int, circular: bool, **kwargs):
        """My cursor"""
        self.curr = 0
        self.max = max
        self.circular = circular
        return super().__init__(**kwargs)

    def reset(self) -> None:
        self.curr = 0

    def next(self) -> None:
        if self.curr == self.max - 1 and self.circular:
            self.curr = 0
        elif self.curr < self.max - 1:
            self.curr += 1

    def prev(self) -> None:
        if self.curr == 0 and self.circular:
            self.curr = self.max - 1
        elif self.curr > 0:
            self.curr -= 1
