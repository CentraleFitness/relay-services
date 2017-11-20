from hardware.oled_128_64 import *
from objects.graphics.gtextbox import *
from objects.graphics.gcontainer import GContainer

if __name__ == "__main__":
    display = Oled_128_64(
        content=GContainer(
            SCREEN_SIZE,
            (0, 0),
            objects=[
                GTextBox((100, 9), (0, 0), "Toto", x=1, y=-1),
                GTextBox((100, 9), (0, 9), "Tata", x=1, y=-1),
                GTextBox((100, 9), (0, 18), "Titi", x=1, y=-1)
                ]))
    display.update_content()
    display.display_content()
