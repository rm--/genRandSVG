'''
Created on Mar 4, 2014

@author: renemuhl
'''

#create random figures, least 4?
#output them as SVG-File
#https://pypi.python.org/pypi/svgwrite/
#sudo pip install svgwrite

import random
import svgwrite
from svgwrite.path import Path
from numpy import absolute

def printNumber(x):
    print(random.randint(0,x))
    

def test():
    dwg = svgwrite.Drawing('test.svg', profile='tiny')
    dwg.add(dwg.line((0, 0), (500, 500), stroke=svgwrite.rgb(255, 255, 200, '%')))
    dwg.add(dwg.ellipse(center=(50,50), r=(100,100)))
    dwg.add(dwg.text('Test', insert=(0, 50), fill='yellow'))
    dwg.save()
    
    
def tryPath():
    #uppercase letter: absolute coords
    p = Path(d=('M', 0, 0))
    print(p.tostring())
    p.push('L', 100, 100)
    p.push('V', 100.7, 200.1)
    p.push('L', 1024, 0)
    p.push('C', 55, 214, 541 ,10 ,50, 50)
    print(p.tostring())
    dwg = svgwrite.Drawing('test.svg', profile='tiny', size=(1024,768))
    dwg.add(p)
    print(dwg.tostring())
    dwg.save()
    
    

    

def addCubicBezier(p, x1, y1, x2, y2, x, y):
    '''
    cubic-bezier-curve ‘c’, ‘C’ (x1 y1 x2 y2 x y)+
    Draws a cubic Bézier curve from the current point to (x,y) using (x1,y1)
    as the control point at the beginning of the curve and (x2,y2) as the
    control point at the end of the curve.
    
    parameters:
    Path p: path object
    [int x, int y] endPoint: end point 
    controlPoint1: 
    controlPoint2:
    '''    
    print(p.toString())
    p.push('C', x1, y1, x2, y2, x, y)
    
    

if __name__ == '__main__':
    tryPath()