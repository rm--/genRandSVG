#!/usr/bin/python
#-*-coding: utf-8 -*-
'''
==========================================================
= author: René Muhl
= from: Leipzig, Germany
= last change: 7.4.2014
= email: ReneM{dot}github{at}gmail{dot}com
==========================================================
===============
= REQUIREMENTS:
= used library: https://pypi.python.org/pypi/svgwrite/
= install with: sudo pip install svgwrite
===============

=> usage: python genRandSVG.py -n 5 -s 1024 768
'''

#2do
######
# install pip in req. ?
# unite the different lines to one method
# need single Elements of one SVG in a list?
# think about contraints to get a distance between points
# develop a general formula for points in a fixed range like the 4 quadrants
# parameter of methods should get the correct range
# cross in the middle test?
# elements in extra module?
# unittests


import argparse
import random
import svgwrite
from svgwrite.path import Path
#import unittest


def main():
    args = parse_arguments()
    countImages = args.n
    width = args.s[0]
    height = args.s[1]
    '''
    numberElementsInSVG < 4 => simple SVG
    numberElementsInSVG < 10 => moderate SVG
    numberElementsInSVG >= 10 => complex SVG
    '''
    numberElementsInSVG = 3

    for i in xrange(countImages):
        print(i)
        s = SVG(i, width, height)
        s.addElement(getRandLine(width, height))
        for _ in xrange(numberElementsInSVG):
            # next element is a line or a cubic bezier
            selection = random.randint(0, 6)
            print("s " + str(selection))
            if(selection == 0):
                s.addElement(getRandLine(width, height))
            elif(selection == 1):
                s.addElement(getRandHorizontalLine(width))
            elif(selection == 2):
                s.addElement(getRandHorizontalLine(height))
            elif(selection == 3):
                s.addElement(getRandCubicBezier(width, height))
            elif(selection == 4):
                s.addElement(getRandSmoothCubicBezier(width, height))
            elif(selection == 5):
                s.addElement(getRandQuadraticBezier(width, height))
            else:
                s.addElement(getRandSmoothQuadraticBezier(width, height))
        s.saveToFile()


def parse_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument("-n", nargs='?', type=int, required=True,
                        help='Integer specifies the number of images.')
    parser.add_argument("-s", nargs=2, type=int, required=True,
        help='Integer specifies the width and height of the images.')
    args = parser.parse_args()
    #print("args: ", args)
    return args


def getRandLine(width, height):
    '''
    line 'l', 'L' (x y)+
    Draw a line from the current point to the given(x, y) coordinate.
    '''
    line = ['L']
    line.append(random.randint(0, width))
    line.append(random.randint(0, height))
    print(line)
    return line


def getRandHorizontalLine(width):
    '''
    horizontal-line 'h', 'H' x+
    Draws a horizontal line from the current point (cpx, cpy) to (x, cpy).
    '''
    line = ['H']
    line.append(random.randint(0, width))
    print(line)
    return line


def getRandVerticalLine(height):
    '''
    vertical-line 'v', 'V' y+
    Draws a vertical line from the current point (cpx, cpy) to (cpx, y).
    '''
    line = ['V']
    line.append(random.randint(0, height))
    print(line)
    return line


def getRandCubicBezier(width, height):
    '''
    cubic-bezier-curve 'c', 'C' (x1 y1 x2 y2 x y)+
    Draws a cubic Bezier curve from the current point to (x,y) using (x1,y1)
    as the control point at the beginning of the curve and (x2,y2) as the
    control point at the end of the curve.

    parameters:
    Path p: path object
    [int x, int y] endPoint: end point
    controlPoint1:
    controlPoint2:
    '''
    bezier = ['C']
    for _ in xrange(3):
        bezier.append(random.randint(0, width))
        bezier.append(random.randint(0, height))
    print(bezier)
    return bezier


def getRandSmoothCubicBezier(width, height):
    '''
    smooth-cubic-bezier-curve 's', 'S' (x2 y2 x y)+
    Draws a cubic Bezier curve from the current point to (x,y). The first
    control point is assumed to be the reflection of the second control
    point on the previous command relative to the current point.
    (If there is no previous command or if the previous command was not
    an C, c, S or s, assume the first control point is coincident with
    the current point.) (x2,y2) is the second control point (i.e., the
    control point at the end of the curve).
    '''
    bezier = ['S']
    for _ in xrange(2):
        bezier.append(random.randint(0, width))
        bezier.append(random.randint(0, height))
    print(bezier)
    return bezier


def getRandQuadraticBezier(width, height):
    '''
    quadratic-bezier-curve 'q', 'Q' (x1 y1 x y)+
    Draws a quadratic Bezier curve from the current point to (x,y) using
    (x1,y1) as the control point.
    '''
    bezier = ['Q']
    for _ in xrange(2):
        bezier.append(random.randint(0, width))
        bezier.append(random.randint(0, height))
    print(bezier)
    return bezier


def getRandSmoothQuadraticBezier(width, height):
    '''
    smooth-quadratic-bezier-curve 't', 'T (x y)+
    Draws a quadratic Bezier curve from the current point to (x,y).
    The control point is assumed to be the reflection of the control
    point on the previous command relative to the current point.
    (If there is no previous command or if the previous command was not
    a Q, q, T or t, assume the control point is coincident with the current
    point.)
    '''
    bezier = ['T']
    bezier.append(random.randint(0, width))
    bezier.append(random.randint(0, height))
    print(bezier)
    return bezier


class SVG:

    ''' SVG '''

    def __init__(self, id, width, height):
        self.id = id
        self.width = width
        self.height = height
        self.path = Path(d=('M', 0, 0))
        self.elements = []

    def addElement(self, newELement):
        self.elements.append(newELement)
        self.path.push(newELement)

    def saveToFile(self):
        dwg = svgwrite.Drawing(str(self.id) + '.svg',
                               profile='tiny', size=(self.width, self.height))
        dwg.add(self.path)
        #print(dwg.tostring())
        dwg.save()


if __name__ == '__main__':
    main()
