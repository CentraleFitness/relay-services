from hardware.oled_128_64 import Oled_128_64 as Oled
from objects.graphics.gtextbox import *

if __name__ == "__main__":
    display = Oled()
    display.content.objects.append(
        GTextBox((128, 10), (0, 0), "Toto", x=10)
        )
    display.update_content()
    display.display_content()
