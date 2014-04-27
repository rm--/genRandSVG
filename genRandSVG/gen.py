#!/usr/bin/python
#-*-coding: utf-8 -*-

import SVG
import random


class generator:
    def __init__(self, WIDTH, HEIGHT, DISTANCE_BETWEEN_POINTS, 
            NUM_ELEMENTS_IN_SVG, MAX_ATTEMPTS_TO_GET_NEW_POINT):
        self.lastPoints = []
        self.WIDTH = WIDTH
        self.HEIGHT = HEIGHT
        self.DBP = DISTANCE_BETWEEN_POINTS
        self.NEIS = NUM_ELEMENTS_IN_SVG
        self.MATOGNP = MAX_ATTEMPTS_TO_GET_NEW_POINT

    def checkNewPoint(self, newX, newY):
        print("new point: (" + str(newX) + ", " + str(newY) + ")")
        for i in range(len(self.lastPoints)):
            inRangeOfX = (newX < self.lastPoints[i][0] + self.DBP
                        and self.lastPoints[i][0] - self.DBP < newX)
            inRangeOfY = (newY < self.lastPoints[i][1] + self.DBP
                        and self.lastPoints[i][1] - self.DBP < newY)

            if(inRangeOfX and inRangeOfY):
                return False
        return True

    def getNewValidPoint(self):
        newX = random.randint(0, self.WIDTH)
        newY = random.randint(0, self.HEIGHT)

        okay = False
        attempt = 0
        while(attempt < self.MATOGNP and not okay):
            okay = self.checkNewPoint(newX, newY)
            #print(okay)
            if(okay):
                break
            else:
                attempt = attempt + 1
            newX = random.randint(0, self.WIDTH)
            newY = random.randint(0, self.HEIGHT)
        newPoint = []
        if(okay):
            newPoint.append(newX)
            newPoint.append(newY)
        return newPoint

    def getRandLine(self):
        '''
        line 'l', 'L' (x y)+
        Draw a line from the current point to the given(x, y) coordinate.
        '''
        line = ['L']
        newPoint = self.getNewValidPoint()
        line.append(newPoint[0])
        line.append(newPoint[1])
        print(line)
        return line

    def getRandBezier(self):
        '''
        A wrapper that returns a quadratic or smooth quadratic, cubic,
        smooth cubic bezier curve.
        Depending on the kind of curve different amount of points must be created.
        '''
        selection = random.randint(0, 3)
        bezier = []
        if(selection == 0):
            bezier = self.getRandQuadraticBezier()
        elif(selection == 1):
            bezier = self.getRandSmoothQuadraticBezier()
        elif(selection == 2):
            bezier = self.getRandCubicBezier()
        else:
            bezier = self.getRandSmoothCubicBezier()
        return bezier

    def getRandCubicBezier(self):
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
        for _ in range(3):
            newPoint = self.getNewValidPoint()
            bezier.append(newPoint[0])
            bezier.append(newPoint[1])
        print(bezier)
        return bezier

    def getRandSmoothCubicBezier(self):
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
        for _ in range(2):
            newPoint = self.getNewValidPoint()
            bezier.append(newPoint[0])
            bezier.append(newPoint[1])
        print(bezier)
        return bezier

    def getRandQuadraticBezier(self):
        '''
        quadratic-bezier-curve 'q', 'Q' (x1 y1 x y)+
        Draws a quadratic Bezier curve from the current point to (x,y) using
        (x1,y1) as the control point.
        '''
        bezier = ['Q']
        for _ in range(2):
            newPoint = self.getNewValidPoint()
            bezier.append(newPoint[0])
            bezier.append(newPoint[1])
        print(bezier)
        return bezier

    def getRandSmoothQuadraticBezier(self):
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
        newPoint = self.getNewValidPoint()
        bezier.append(newPoint[0])
        bezier.append(newPoint[1])
        print(bezier)
        return bezier

    def createNewSVG(self, i):
        s = SVG.SVG(i, self.WIDTH, self.HEIGHT)
        s.addElement(self.getRandLine())
        for _ in range(self.NEIS):
            print("previous elements: " + str(s.getElements()))
            self.lastPoints = s.getPreviousPoints()
            # roll the dice to get next element (line or bezier curve)
            selection = random.randint(0, 2)
            #print("elment " + str(selection))
            if(selection == 0):
                s.addElement(self.getRandLine())
            else:
                s.addElement(self.getRandBezier())
        s.saveToFile()
