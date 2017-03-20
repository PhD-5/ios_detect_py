from clint.textui import colored, puts
import sys
import time
import curses


if __name__ == '__main__':
    for color in colored.COLORS:
        puts(getattr(colored, color)("Text in {0:s}".format(color.upper())))

    # sys.stdout.write('\r')
    # time.sleep(5)
    # sys.stdout.flush()
    # sys.stdout.write('some data')
    # time.sleep(5)
    # sys.stdout.flush()
    # sys.stdout.write('other different data')
    # sys.stdout.flush()

    stdscr = curses.initscr()