#!/bin/env python3

import argparse
import random
import subprocess

COLORS = range(41, 48)
choice = random.choice
clear = lambda: subprocess.call('clear')
echo = lambda s: print(s, end="")
block = lambda color, size: "\033[0;{}m{}".format(color, " " * size)
termxy = lambda: map(int, subprocess.check_output(['stty','size']).split())
showcur = lambda vis: echo('\033[?25{}'.format('h' if vis else 'l'))
color = lambda row_color, gap, same: \
    40 if random.random() <= gap else row_color if same else choice(COLORS)

def distribute(min, max, total, current=0):
    """
    generate a list of numbers between `min` and `max` that adds up to `total`
    """
    if current == total:
        return [0]
    if (total - current) < (max):
        return [total - current]
    block = choice(range(min, max+1))
    return [block] + distribute(min, max, total, current+block)

def blocks(min, max, gap, same):
    """
    the width and height of the terminal is calculated, and then a distribution
    of blocks is calculated and printed to perfectly fill the terminal
    """
    if min > max:
        raise ValueError('min-width must be less than or equal to max-width')  
    try:
        rows, cols = termxy()
        for row in range(rows):
            row_color = choice(COLORS)
            for size in distribute(min, max, cols):
                echo(block(color(row_color, gap, same), size)) 

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
    add('-min',help="set the min width of a block",type=int,default=2)
    add('-max',help="set the max width of a block",type=int,default=10)
    add('-gap',help='probablility of a block being a gap',type=float,default=0.3)
    add('-same',help="make all blocks within a row have the same color",action='store_true')
    blocks(**vars(parser.parse_args()))
