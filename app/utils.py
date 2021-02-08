
# Text functions
Reset = '\033[0m'
Bold = '\033[1m'
Underline = '\033[4m'
Reversed = '\033[7m'

# Basic 8 colors
Black = '\033[30m'
Red = '\033[31m'
Green = '\033[32m'
Yellow = '\033[33m'
Blue = '\033[34m'
Magenta = '\033[35m'
Cyan = '\033[36m'
White = '\033[37m'

# Extended 16 colors
BrightBlack = Gray = '\033[30;1m'
BrightRed = '\033[31;1m'
BrightGreen = '\033[32;1m'
BrightYellow = '\033[33;1m'
BrightBlue = '\033[34;1m'
BrightMagenta = '\033[35;1m'
BrightCyan = '\033[36;1m'
BrightWhite = '\033[37;1m'


def colorizeValue(value, suffix="", positiveColor=None):
    if value == 0: return '•'
    if positiveColor is None: positiveColor = Green
    sign_str = ("-" if value < 0 else "+")
    value_str = str(round(abs(value), 2))
    color_str = Red if value < 0 else positiveColor
    return (color_str, sign_str+value_str+suffix)

def printRow(*cells, color='', sizes=[]):
    if color is not None: print(color, end='')
    for i, cell in enumerate(cells):
        print(' ', end='')
        if isinstance(cell, tuple):
            print(cell[0] + cell[1].ljust(sizes[i]) + Reset, end='')
        else:
            print(cell.ljust(sizes[i]), end='')
    print('' if color is None else Reset)