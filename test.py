from display.oled_128_64 import Oled_128_64 as Oled

if __name__ == "__main__":
    display = Oled()
    display.display_content()
    input()
