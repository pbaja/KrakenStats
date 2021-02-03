
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

# Pretty print profit/loss
def prettyFormat(value, prefix='', suffix='', minlen=0, positiveColor=None):
    if positiveColor is None: positiveColor = Green
    sign_str = ("-" if value < 0 else "+")
    value_str = round(abs(value), 2)
    color_str = Red if value < 0 else positiveColor
    content = f'{prefix}{sign_str} {value_str}{suffix}'.ljust(minlen)
    return f"{color_str}{content}{Reset}"

def printTable(array):
    for r, row in enumerate(array):
        # Build line
        line = ''
        for c, item in enumerate(row):
            line += item
        print(line)