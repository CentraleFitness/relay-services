import platform

from .dynamo import Dynamo

if platform.system() != 'Windows':
    from .joystick import Joystick
    from .oled_128_64 import Oled_128_64
    from .pushbutton import Pushbutton
