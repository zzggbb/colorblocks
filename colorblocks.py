#!/bin/env python3

import argparse
import random
import subprocess

COLORS = range(31, 38)
clear = lambda: subprocess.call(['tput','reset'])
echo = lambda s: print(s, end="")
termxy = lambda: map(int, subprocess.check_output(['stty','size']).split())
showcur = lambda vis: echo('\033[?25{}'.format('h' if vis else 'l'))

def block(gap, size, row_color, same, char):
    """
    generate a block, which is either a space (" ") colored with the default
    background color, or a char (defaults to ▉) colored with a random color.
    """
    colored = gap <= random.random()
    color = 49 if not colored else row_color if same else random.choice(COLORS)
    char = char if colored else " "
    return "\033[0;{}m{}".format(color, char * size)

def distribute(min, max, total, current=0):
    """
    generate a list of numbers between `min` and `max` that adds up to `total`
    """
    if total - current < max:
        return [total - current]
    block = random.choice(range(min, max+1))
    return [block] + distribute(min, max, total, current+block)

def blocks(min, max, gap, same, char):
    """
    the width and height of the terminal is calculated, and then a distribution
    of blocks is calculated and printed to perfectly fill the terminal
    """
    if min > max:
        raise ValueError('min-width must be less than or equal to max-width')  
    rows, cols = termxy()
    try:
        for row in range(rows):
            row_color = random.choice(COLORS)
            for size in distribute(min, max, cols):
                echo(block(gap, size, row_color, same, char))

        showcur(False)
        input()
    except KeyboardInterrupt:
        pass
    finally:
        showcur(True)
        clear()

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    add = parser.add_argument
    add('-min',help="set the min width of a block",type=int,default=4)
    add('-max',help="set the max width of a block",type=int,default=10)
    add('-gap',help='probablility of a block being a gap',type=float,default=0.3)
    add('-same',help="make all blocks within a row have the same color",action='store_true')
    add('-char',help="the character that composes a block, default is a block",default="▉")
    blocks(**vars(parser.parse_args()))
