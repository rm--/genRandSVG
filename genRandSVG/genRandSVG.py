'''
Created on Mar 4, 2014

@author: renemuhl
'''
# used lib: https://pypi.python.org/pypi/svgwrite/
# install with: sudo pip install svgwrite
# usage: python genRandSVG.py -n 5 -s 1024 768


#2do
######
# create random figures, least 4?
# output them as SVG-File
# class with parameter picture size
# getter for length and width
# save single elements like cubicBezier, line etc..

import argparse
import random
import svgwrite
from svgwrite.path import Path


def main():
    args = parse_arguments()
    countImages = args.n
    width = args.s[0]
    height = args.s[1]

    for i in range(countImages):
        print(i)
        s = SVG(i, width, height)
        s.addElement(getRandLine(width, height))
        s.addElement(['V', 100.7])
        s.addElement(['L', 1024, 0])
        s.addElement(getRandCubicBezier(width, height))
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
    for i in range(6):
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
