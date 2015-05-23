#!/bin/env python3

import argparse
import random
import subprocess

clear = lambda: subprocess.call('clear')
echo = lambda s: print(s, end="")

def distribute(min, max, total, current):
    """
    generate a list of numbers between `min` and `max` 
    until they add up to `total`
    """
    if current == total:
        return [0]
    if (total - current) < (max):
        return [total - current]
    block = random.randrange(min, max+1)
    return [block] + distribute(min, max, total, current+block)

def block(color, size):
    return "\033[0;{}m{}".format(color, " " * size) 

def blocks(max_width, min_width, color_same_row, gap_prob):
    """
    output the blocks
    the width and height of the terminal is calculated, and then a distribution
    of blocks is calculated and printed to perfectly fill the terminal
    """
    clear()
    rows, cols = map(int, subprocess.check_output(['stty','size']).split())
    colors = range(41, 48)
    for row in range(rows):
        blocks = distribute(min_width, max_width, cols, 0)
        random.shuffle(blocks)
        row_color = random.choice(colors)
        for size in blocks:
            gap = random.random() <= gap_prob
            color = row_color if color_same_row else (40 if gap else random.choice(colors))
            code = block(color, size) 
            echo(code) 
    echo('\033[?25l')
    input()
    echo('\033[?25h')

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--max-width','-max',help="set max width of a block",type=int,default=10)
    parser.add_argument('--min-width','-min',help="set the min width of a block",type=int,default=2)
    parser.add_argument('--color-same-row','-s',help="limit color randomness to be between rows, instead of within rows",action='store_true')
    parser.add_argument('--gap-prob','-gp',help='probablility of a block being a gap',type=float,default=0.3)
    args = parser.parse_args()
    blocks(**vars(args))
