#!/bin/env python3

import argparse
import random
import subprocess

COLORS = range(41, 48)
clear = lambda: subprocess.call('clear')
echo = lambda s: print(s, end="")
block = lambda color, size: "\033[0;{}m{}".format(color, " " * size)
termxy = lambda: map(int, subprocess.check_output(['stty','size']).split())
showcur = lambda vis: echo('\033[?25{}'.format('h' if vis else 'l'))
get_color = lambda row_color, gap, row: \
    40 if random.random() <= gap else row_color if row else random.choice(COLORS)

def distribute(min, max, total, current):
    """
    generate a list of numbers between `min` and `max` that add up to `total`
    """
    if current == total:
        return [0]
    if (total - current) < (max):
        return [total - current]
    block = random.randrange(min, max+1)
    return [block] + distribute(min, max, total, current+block)

def blocks(min, max, same, gap):
    """
    the width and height of the terminal is calculated, and then a distribution
    of blocks is calculated and printed to perfectly fill the terminal
    """
    if min > max:
        raise ValueError('min-width must be less than or equal to max-width')  
    try:
        rows, cols = termxy()
        for row in range(rows):
            blocks = distribute(min, max, cols, 0)
            random.shuffle(blocks)
            row_color = random.choice(COLORS)
            for size in blocks:
                color = get_color(row_color, gap, same)
                echo(block(color, size)) 

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
    add('-max',help="set max width of a block",type=int,default=10)
    add('-same',help="make all blocks within a row have the same color",action='store_true')
    add('-gap',help='probablility of a block being a gap',type=float,default=0.3)
    blocks(**vars(parser.parse_args()))
