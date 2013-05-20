#!/usr/bin/python
# -*- coding: utf-8 -*-

#=========================================================
#author: René Muhl
#from: Leipzig, Germany
#last change: 20.5.2013
#email: ReneM{dot}github{at}gmail{dot}com
#=========================================================

#requirements:
#[library]
## --> get library:
### https://code.google.com/p/svgfig/wiki/RevisionHistory?tm=2
## --> unpack, go to folder and install library with:
### sudo python setup.py install
## if it doesn't work, try this instructions:
### https://code.google.com/p/svgfig/wiki/HowToInstall
#######
#[images]
## --> image must be plainSVG
## --> please disable "Allow relative coordinates"at File-Inkscape Preferences-SVG output
### after that images shouldn't have relative coordinates


"""
	2do:
	#conventions variablenames
	#copy SVG object and work with it
	#trying DOM or another XML parse technology
"""

import svgfig  		#parse SVG
import random 		#random numbers gen
import ast 			#convert unicode in int/float
import datetime 	#current date/time
import math 		#sqrt(), pow()
import sys 			#exit function
import os 			#system function like create folder
#import re 			#regex
#import copy		#copy Objects

####################################
#########params
####################################

###
SVGInput_FileName="plainSVG5.svg"
outputDir = "output"
#SVGOutput_FileNameTemplate="genSVG"
numImages=150
substitutionPercent=.5				#specifies how many Coord be replaced

#DIN A4:(744,1052)
imageSizeX=744
imageSizeY=1052
###

###
#for area test
minimumAreaPercentX=.4
minimumAreaPercentY=.4

#a number between 1-4
pointsMustBeInQuadrants=3
###

###
#for distance test
#value in pixel (recommended max. 180)
minimumDistanceTwoPoints=140
###

####################################
#########functions
####################################

def loadSVGandGetXML(filename):
	#test if file exists
	SVGobj = svgfig.load(filename)
	return SVGobj


def getPathD_asList(SVGobj):
	try:
		#print SVGobj[2,0,u'd'],"\n\n\n\n"
		SVGpathD=SVGobj[2,0,u'd']
	except:
	 	#print SVGobj[2,u'd'],"\n\n\n\n"
	 	try:
			SVGpathD=SVGobj[2,u'd']
		except:
			print "The picture seems to be stored as InkscapeSVG, please save it as PlainSVG and start the program again."
			sys.exit()

	#print SVGpathD,"\n"
	d_List = unicode.split(SVGpathD)	#split() returns a list of esments
										#which are seperated by spaces(default) in the original string
	return d_List


def getNumberOfCoords(d_List):
	numCoords=0
	for el in d_List:
		if not el[0].isalpha():
			#print el, "\n"
			numCoords+=1
	return numCoords


def getRandomIndex(numCoords):
	# obtain the random index to be replaced 
	while True:
		randIndex=random.randint(0,numCoords)
		inList=isIndexInList(randIndex,indexList)
		if inList:
			continue
		else:
			indexList.append(randIndex)
			break
	return randIndex


#start and stop has a connection to width and height
# get two random coordinates 
# up to now with fixed range
def getRandomCoords():
	rand1=random.uniform(xstart,xstop)
	rand2=random.uniform(ystart,ystop)
	#validate coords with a seperate function/strategy
	#print "rand1 rand2: ", rand1, rand2, "\n"
	randCoords=unicode(rand1) + "," + unicode(rand2)
	return randCoords


def print_d_List(d_List):
	for index in range(0,len(d_List)):
		print "dlist[",index,"]: ",d_List[index],"\n"

 		
def substituteCoordsAndGet_d_List(d_List,randIndex,randCoords):			#call by value or call by reference?
	numCoords=0
	for index in range(0,len(d_List)):
		#print d_List[index][0].isalpha()
		if not d_List[index][0].isalpha():
			#print randIndex,numCoords, "\n"
			if numCoords == randIndex:
				#print "=========>",d_List[index], "\n"
				d_List[index]=randCoords
				#print "===============>",d_List[index], "\n"
				break
			else:
				numCoords+=1
	return d_List


def transform_d_List_toPathD_AndGet(d_List):
	newPathD = ""
	for newDListEl in d_List:
		if d_List[len(d_List)-1] == newDListEl:
			newPathD += newDListEl
		else:
			newPathD += newDListEl
			newPathD += " "
	return newPathD


def modifySVGAndSave(newPathD,SVGobj):
	try:
		SVGobj[2,0,u'd']=newPathD
	except IndexError:
		SVGobj[2,u'd']=newPathD
		now = datetime.datetime.now()

	outputFileName="./output/"+str(now)+".svg"
	print outputFileName,"\n========================\n"
	SVGobj.save(outputFileName)


#Indices that have been used should be used a second time
def isIndexInList(index,indexList):
	if index in indexList:
		return True
	else:
		return False		


#Test whether the image braced a minimum area size.
#explanation....
def areaTest(d_List):
	testLeftBelow=False
	testLeftTop=False
	testRightTop=False
	testRightBelow=False

	testSuccess=False
	pointsInQuadrants=0
	for index in range(0,len(d_List)):
		if not d_List[index][0].isalpha():
			#print "num:",d_List[index]
			testCoord = unicode.split(d_List[index],",")
			coordX=ast.literal_eval(testCoord[0])
			coordY=ast.literal_eval(testCoord[1])
			if not testLeftBelow and (coordX < X_leftLimit and coordY < Y_belowLimit):
				testLeftBelow=True
				pointsInQuadrants+=1
			if not testLeftTop and (coordX < X_leftLimit and coordY > Y_topLimit):
				testLeftTop=True
				pointsInQuadrants+=1
			if not testRightTop and (coordX > X_rightLimit and coordY > Y_topLimit):
				testRightTop=True
				pointsInQuadrants+=1
			if not testRightBelow and (coordX > X_rightLimit and coordY < Y_belowLimit):
				testRightBelow=True
				pointsInQuadrants+=1

		#print "pointsMustBeInQuadrants:",pointsMustBeInQuadrants
		#print "pointsInQuadrants:",pointsInQuadrants
		if pointsInQuadrants >= pointsMustBeInQuadrants:
			testSuccess=True
			break

	return testSuccess


#To reduce acute, slender figure parts, a minimum distance between all points must be met.
def distanceTest(d_List):
	testSuccess=True
	allCoords=[]
	distance=0
	for index1 in range(0,len(d_List)):
		if not d_List[index1][0].isalpha():
			#print "num1:",d_List[index1]
			testCoord1 = unicode.split(d_List[index1],",")
			coordX1=ast.literal_eval(testCoord1[0])
			coordY1=ast.literal_eval(testCoord1[1])
			for index2 in range(0,len(d_List)):
				if index1 != index2 and not d_List[index2][0].isalpha():
					#print "num2:",d_List[index2]
					testCoord2 = unicode.split(d_List[index2],",")
					coordX2=ast.literal_eval(testCoord2[0])
					coordY2=ast.literal_eval(testCoord2[1])
					distance=math.sqrt(math.pow(coordX2-coordX1,2)+math.pow(coordY2-coordY1,2))
					#print "distance:",distance
					if distance != 0 and distance<minimumDistanceTwoPoints:
						testSuccess=False
						break

	return testSuccess


####################################
#########main program
####################################

#Check if folder exists, if not then it will be created.
path = "." + os.sep + outputDir
if not os.path.exists(path):
	print "dir doesn't exists"
	os.mkdir(path)
	print "output directory \" "+ outputDir +" \"created."
else:
    print "dir exists"

	
#ranges of randomCoords
# randomX (xstart,xstop)
# randomY (ystart,ystop)
xstart=imageSizeX*0.02
print xstart
xstop=imageSizeX*0.98
print xstop

ystart=imageSizeY*0.02
print ystart
ystop=imageSizeY*0.98
print ystop


#Calculate the limits of the test area
X_rightLimit=imageSizeX*(minimumAreaPercentX+(1-minimumAreaPercentX)/2)
print X_rightLimit
X_leftLimit=imageSizeX*(1-minimumAreaPercentX)/2
print X_leftLimit

Y_topLimit=imageSizeY*(minimumAreaPercentY+(1-minimumAreaPercentY)/2)
print Y_topLimit
Y_belowLimit=imageSizeY*(1-minimumAreaPercentY)/2
print Y_belowLimit


for currentImg in range(1,numImages+1):	

	testSuccess1=False
	testSuccess2=False
	while not testSuccess1 or not testSuccess2:
		print "\n :::::::: new try.... :::::::: \n"
		indexList = []
		SVGobj=loadSVGandGetXML(SVGInput_FileName)
		#print "SVGobj:",SVGobj

		d_List=getPathD_asList(SVGobj)
		#print "d_List:",d_List

		numCoords=getNumberOfCoords(d_List)
		#print "numCoords:",numCoords

		numSubstitutions=int(numCoords*substitutionPercent)
		print "numSubstitutions:",numSubstitutions
		if numSubstitutions == 0:
			print "The number of points to be replaced is too small, please change the \"numSubstitutions\" parameter."
		else:
			for coordNum in range(0,numSubstitutions):
				
				randIndex=getRandomIndex(numCoords)
				#print "randIndex",coordNum,": ",randIndex
				
				randCoords=getRandomCoords()
				print "randCoords",coordNum,":" ,randCoords,"\n"

				#print_d_List(d_List)
				d_List = substituteCoordsAndGet_d_List(d_List,randIndex,randCoords)
				#print_d_List(d_List)

				newPathD = transform_d_List_toPathD_AndGet(d_List)
				#print newPathD

			testSuccess1=areaTest(d_List)
			testSuccess2=distanceTest(d_List)
			#print "testSuccess1:",testSuccess1
			#print "testSuccess2:",testSuccess2
			if testSuccess1 and testSuccess2:
				modifySVGAndSave(newPathD,SVGobj)
