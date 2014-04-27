#!/usr/bin/python
#-*-coding: utf-8 -*-

import svgwrite
from svgwrite.path import Path
import os
import random


class SVG:

    ''' SVG '''

    def __init__(self, id, WIDTH, HEIGHT):
        self.id = id
        self.WIDTH = WIDTH
        self.HEIGHT = HEIGHT
        x = random.randint(0, self.WIDTH)
        y = random.randint(0, self.HEIGHT)
        self.path = Path(d=('M', x, y))
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
        for i in range(len(self.elements)):
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
