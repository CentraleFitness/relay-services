"""Description of the class"""

class LineManager:
    """Definition of the class"""
    def __init__(self, max_lines=1):
        """Manager the number of lines the display can handle"""
        assert max_lines > 0
        self.lines = list()
        self.max_lines = max_lines

    def add_line(self, line):
        """
        Add a line to the display
        Remove an older one if there is too many
        """
        self.lines.append(line)
        if len(self.lines) > self.max_lines:
            del self.lines[0]

    def get_lines(self):
        """Enumerate each line availables"""
        return enumerate(self.lines)

    def delete_all_lines(self, *args):
        """Delete all the lines saved in the linemanager"""
        self.lines.clear()

    def delete_line(self, lines: list):
        """
        Delete a single or more lines
        params: a list of lines to delete
        """
        for line in lines:
            if line > self.max_lines - 1:
                raise IndexError("LineManager: Line out of range")
            del self.lines[line]

    def delete_line_range(self, line_range: list) -> None:
        """
        Delete a range of lines
        params: a list of two lines to form a range [from, to]
        warning: line_to non inclusive
        """
        if line_range[0] < 0 or line_range[1] > self.max_lines - 1:
            raise IndexError("LineManager: Lines out of range")
        del self.lines[line_range[0]:line_range[1]]
