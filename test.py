from hardware.oled_128_64 import *
from objects.graphics.gtextbox import *
from objects.graphics.gcontainer import GContainer

import RPi.GPIO as GPIO

L_pin = 27
R_pin = 23
C_pin = 4
U_pin = 17
D_pin = 22

A_pin = 5
B_pin = 6

INPUTS = {
    L_pin: False,
    R_pin: False,
    C_pin: False,
    U_pin: False,
    D_pin: False,
    A_pin: False,
    B_pin: False
}


GPIO.setmode(GPIO.BCM)
GPIO.setup(A_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(B_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(L_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(R_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(U_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(D_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(C_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)


if __name__ == "__main__":

    while True:
        for _input in INPUTS:
            if not GPIO.input(_input) and not INPUTS[_input]:
                INPUTS[_input] = not INPUTS[_input]
                print("{} pressed".format(_input))
            elif GPIO.input(_input) and INPUTS[_input]:
                INPUTS[_input] = not INPUTS[_input]
                print("{} released".format(_input))
                
    
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
