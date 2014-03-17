#!/usr/bin/python
#-*-coding: utf-8 -*-
'''
==========================================================
= author: René Muhl
= from: Leipzig, Germany
= last change: 17.4.2014
= email: ReneM{dot}github{at}gmail{dot}com
==========================================================
===============
= REQUIREMENTS:
= used library: https://pypi.python.org/pypi/svgwrite/
= documentation: http://pythonhosted.org//svgwrite/index.html
= install with: sudo pip install svgwrite
===============

=> usage: python genRandSVG.py -n 5 -s 1280 1024
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
# new command line args distance and attempts -> access?
# unittests


import argparse
import random
import svgwrite
from svgwrite.path import Path
import os
import sys
#import unittest

DISTANCE_BETWEEN_POINTS = 300
MAX_ATTEMPTS_TO_GET_NEW_POINT = 30


def main():
    args = parse_arguments()
    numberImages = args.n
    WIDTH = args.s[0]
    HEIGHT = args.s[1]
    '''
    numberElementsInSVG < 4 => simple SVG
    numberElementsInSVG < 10 => moderate SVG
    numberElementsInSVG >= 10 => complex SVG
    '''
    numberElementsInSVG = 3

    ENOUGH_SPACE_IN_X = WIDTH / DISTANCE_BETWEEN_POINTS < numberElementsInSVG
    ENOUGH_SPACE_IN_Y = HEIGHT / DISTANCE_BETWEEN_POINTS < numberElementsInSVG
    if(ENOUGH_SPACE_IN_X or ENOUGH_SPACE_IN_Y):
        print("DISTANCE_BETWEEN_POINTS too big for this numberElementsInSVG!"
                                                            " Will now stop.")
        sys.exit(-1)

    for i in xrange(numberImages):
        print("SVG #" + str(i))
        s = SVG(i, WIDTH, HEIGHT)
        s.addElement(getRandLine(WIDTH/numberElementsInSVG,
                                 HEIGHT/numberElementsInSVG))
        lastPoints = []
        for _ in xrange(numberElementsInSVG):
            print("previous elements: " + str(s.getElements()))
            lastPoints = s.getPreviousPoints()
            # roll the dice to get next element (line or bezier curve)
            selection = random.randint(0, 4)
            #print("elment " + str(selection))
            if(selection == 0):
                s.addElement(getRandLine(WIDTH, HEIGHT, lastPoints))
            elif(selection == 1):
                s.addElement(getRandCubicBezier(WIDTH, HEIGHT, lastPoints))
            elif(selection == 2):
                s.addElement(getRandSmoothCubicBezier(WIDTH, HEIGHT, lastPoints))
            elif(selection == 3):
                s.addElement(getRandQuadraticBezier(WIDTH, HEIGHT, lastPoints))
            else:
                s.addElement(getRandSmoothQuadraticBezier(WIDTH, HEIGHT, lastPoints))
        s.saveToFile()


def parse_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument("-n", nargs='?', type=int, required=True,
                        help='Integer specifies the number of images.')
    parser.add_argument("-s", nargs=2, type=int, required=True,
        help='Integer specifies the WIDTH and HEIGHT of the images.')
    args = parser.parse_args()
    #print("args: ", args)
    return args


def checkNewPoint(lastPoints, newX, newY):
    flag = True
    print("new point: (" + str(newX) + ", " + str(newY) + ")")
    for i in xrange(len(lastPoints)):
        inRangeOfX = (newX < lastPoints[i][0] + DISTANCE_BETWEEN_POINTS
                    and lastPoints[i][0] - DISTANCE_BETWEEN_POINTS < newX)
        inRangeOfY = (newY < lastPoints[i][1] + DISTANCE_BETWEEN_POINTS
                    and lastPoints[i][1] - DISTANCE_BETWEEN_POINTS < newY)

        if(inRangeOfX and inRangeOfY):
            flag = False
            break
    return flag


def getNewValidPoint(WIDTH, HEIGHT, lastPoints=[]):
    newX = random.randint(0, WIDTH)
    newY = random.randint(0, HEIGHT)

    okay = False
    attempt = 0
    while(attempt < MAX_ATTEMPTS_TO_GET_NEW_POINT and not okay):
        okay = checkNewPoint(lastPoints, newX, newY)
        #print(okay)
        if(okay):
            break
        else:
            attempt = attempt + 1
        newX = random.randint(0, WIDTH)
        newY = random.randint(0, HEIGHT)
    newPoint = []
    if(okay):
        newPoint.append(newX)
        newPoint.append(newY)
    return newPoint


def getRandLine(WIDTH, HEIGHT, lastPoints=[]):
    '''
    line 'l', 'L' (x y)+
    Draw a line from the current point to the given(x, y) coordinate.
    '''
    line = ['L']
    newPoint = getNewValidPoint(WIDTH, HEIGHT, lastPoints)
    line.append(newPoint[0])
    line.append(newPoint[1])
    print(line)
    return line


def getRandCubicBezier(WIDTH, HEIGHT, lastPoints):
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
        newPoint = getNewValidPoint(WIDTH, HEIGHT, lastPoints)
        bezier.append(newPoint[0])
        bezier.append(newPoint[1])
    print(bezier)
    return bezier


def getRandSmoothCubicBezier(WIDTH, HEIGHT, lastPoints):
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
        newPoint = getNewValidPoint(WIDTH, HEIGHT, lastPoints)
        bezier.append(newPoint[0])
        bezier.append(newPoint[1])
    print(bezier)
    return bezier


def getRandQuadraticBezier(WIDTH, HEIGHT, lastPoints):
    '''
    quadratic-bezier-curve 'q', 'Q' (x1 y1 x y)+
    Draws a quadratic Bezier curve from the current point to (x,y) using
    (x1,y1) as the control point.
    '''
    bezier = ['Q']
    for _ in xrange(2):
        newPoint = getNewValidPoint(WIDTH, HEIGHT, lastPoints)
        bezier.append(newPoint[0])
        bezier.append(newPoint[1])
    print(bezier)
    return bezier


def getRandSmoothQuadraticBezier(WIDTH, HEIGHT, lastPoints):
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
    newPoint = getNewValidPoint(WIDTH, HEIGHT, lastPoints)
    bezier.append(newPoint[0])
    bezier.append(newPoint[1])
    print(bezier)
    return bezier


class SVG:

    ''' SVG '''

    def __init__(self, id, WIDTH, HEIGHT):
        self.id = id
        self.WIDTH = WIDTH
        self.HEIGHT = HEIGHT
        self.path = Path(d=('M', 0, 0))
        self.elements = []

    def addElement(self, newELement):
        self.elements.append(newELement)
        self.path.push(newELement)

    def getElements(self):
        return self.elements

    def getPointOfLastElement(self):
        point = []
        #print(self.elements[-1])
        point.append(self.elements[-1][-2])
        point.append(self.elements[-1][-1])
        return point

    def getPreviousPoints(self):
        points = []
        for i in xrange(len(self.elements)):
            points.append([self.elements[i][-2], self.elements[i][-1]])
        print("previous points: " + str(points))
        return points

    def saveToFile(self):
        OUTPUT_DIR = "output"
        #Check if folder exists, if not then it will be created.
        path = "." + os.sep + OUTPUT_DIR + os.sep
        try:
            os.makedirs(path)
        except OSError:
            if os.path.exists(path):
                # We are nearly safe
                pass
            else:
                # There was an error on creation, so make sure we know about it
                raise
        dwg = svgwrite.Drawing(path + str(self.id) + '.svg',
                               profile='tiny', size=(self.WIDTH, self.HEIGHT))
        dwg.add(self.path)
        #print(dwg.tostring())
        dwg.save()


if __name__ == '__main__':
    main()
