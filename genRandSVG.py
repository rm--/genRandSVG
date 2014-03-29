#!/usr/bin/python
#-*-coding: utf-8 -*-

'''
==========================================================
= author: René Muhl
= from: Leipzig, Germany
= last change: 29.4.2014
= email: ReneM{dot}github{at}gmail{dot}com
==========================================================
===============
= REQUIREMENTS:
= used library: https://pypi.python.org/pypi/svgwrite/
= documentation: http://pythonhosted.org//svgwrite/index.html
= install with: sudo pip install svgwrite
===============

=> usage: python genRandSVG.py -n 15 -s 1280 1024 -el 4 -d 100 -a 15
or
=> usage: python genRandSVG.py -n 15 -s 1280 1024
'''

#2do
######
# install pip in req. ?
# need single Elements of one SVG in a list?
# think about contraints to get a distance between points
# develop a general formula for points in a fixed range like the 4 quadrants
# cross in the middle test?
# what happens when more attempts as max attempts - need sophisticated solution?! :D
# documentation
# different examples with args and results
# unittests/pytest! - in extra package?


import argparse
import sys
import gen
#import unittest


def main():

    args = parse_arguments()
    numberImages = args.n
    WIDTH = args.s[0]
    HEIGHT = args.s[1]
    DISTANCE_BW_POINTS = args.d
    NUM_ELEMENTS_IN_SVG = args.el
    MAX_ATTEMPTS_TO_GET_NEW_POINT = args.a

    if(not args.d):
        DISTANCE_BW_POINTS = 1

    if (args.el):
        ENOUGH_SPACE_IN_X = WIDTH / DISTANCE_BW_POINTS < NUM_ELEMENTS_IN_SVG
        ENOUGH_SPACE_IN_Y = HEIGHT / DISTANCE_BW_POINTS < NUM_ELEMENTS_IN_SVG
        if(ENOUGH_SPACE_IN_X or ENOUGH_SPACE_IN_Y):
            print("Distance between points too big for this amount of elements "
                "and resolution!\nPlease decrease distance or count of elements. "
                        "Another option is to increase the resolution.\nWill now stop.")
            sys.exit(-1)
    else:
        # calculate the optimal amount of elements for this width and height ?
        NUM_ELEMENTS_IN_SVG = 4

    if (not args.a):
        MAX_ATTEMPTS_TO_GET_NEW_POINT = 30


    g = gen.generator(WIDTH, HEIGHT, DISTANCE_BW_POINTS, NUM_ELEMENTS_IN_SVG,
                                                 MAX_ATTEMPTS_TO_GET_NEW_POINT)
    for i in xrange(numberImages):
        print("SVG #" + str(i))
        g.createNewSVG(i)


def parse_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument("-n", nargs='?', type=int, required=True,
                        help='Integer specifies the number of images.')
    parser.add_argument("-s", nargs=2, type=int, required=True,
        help='Integer specifies the width and height of the images.')
    parser.add_argument("-el", nargs='?', type=int, required=False,
        help='Integer specifies the number of elements that should be created.\n'
        'el < 4 => simple SVG\n'
        'el < 10 => moderate SVG\n'
        'el >= 10 => complex SVG\n')
    parser.add_argument("-d", nargs='?', type=int, required=False,
        help='Integer specifies the distance between the new points and all '
        'previous points.')
    parser.add_argument("-a", nargs='?', type=int, required=False,
        help='Integer specifies the number of attempt to get a new point '
        'with correct distance to all previous points.')
    args = parser.parse_args()
    print("args: ", args)
    return args


if __name__ == '__main__':
    main()
