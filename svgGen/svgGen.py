#!/usr/bin/python
# -*- coding: utf-8 -*-

#install lib: sudo python setup.py install
#works only with plainSVG


# 2do:
	#Image should have a minimum area
	#test if file exists
	#test with plain and inkscape SVG
	#conventions variablenames
	# distinguish between width and height (different maxima)
	## if the el.isalpha == true -> roll the dice again
	# create structure with methods, commandline arguments like input, number - really necessary?
	## of SVGs to be generated
	#http://de.wikipedia.org/wiki/Gau%C3%9Fsche_Trapezformel
	#https://code.google.com/p/svgfig/wiki/HowToInstall

import svgfig  		#parse SVG
import random 		#random numbers gen
#import re 			#regex
#import copy		#copy Objects
#from sets import set 
import ast
import datetime
from os import *	#system function like create folder


####################################
#########params
####################################

SVGInput_FileName="plainSVG2.svg"
#SVGOutput_FileNameTemplate="genSVG"
numImages=5
substitutionPercent=.4				#specifies how many Coord be replaced

#DIN A4:(744,1052)
imageSizeX=744
imageSizeY=1052


minimumAreaPercentX=.3
minimumAreaPercentY=.3
#PercentPointsInQuadrants=.4
pointsMustBeInQuadrants=4

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
	except IndexError:
	 	#print SVGobj[2,u'd'],"\n\n\n\n"
		SVGpathD=SVGobj[2,u'd']
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


#The letters must be capitalized, otherwise you have no absolute coordinates.
#When using the absolute coordinates must be made negative to positive, as they would otherwise not on the image.
def normalizeSVG(d_List):
	for index in range(0,len(d_List)):
		if d_List[index].isupper():
			continue
		elif d_List[index][0].isalpha() and d_List[index].islower():
			#print "alpha:",d_List[index]
			d_List[index]=unicode.upper(d_List[index][0])
		else:
			#print "!alpha:",d_List[index]
			testCoord = unicode.split(d_List[index],",")
			#print "testCoord:", testCoord
			coord1=ast.literal_eval(testCoord[0])
			if coord1 < 0:
				#print "neg:",coordX
				coord1=-coord1
			coord2=ast.literal_eval(testCoord[1])
			if coord2 < 0:
				#print "neg:",coord2
				coord2=-coord2
			d_List[index]=str(coordX) + "," + str(coord2)
	newPathD = transform_d_List_toPathD_AndGet(d_List)
	
	try:
		SVGobj[2,0,u'd']=newPathD
	except IndexError:
		SVGobj[2,u'd']=newPathD
	SVGobj.save(SVGInput_FileName)


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
			print "num:",d_List[index]
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

		print "pointsInQuadrants:",pointsInQuadrants
		if pointsInQuadrants >= pointsMustBeInQuadrants:
			testSuccess=True
			break

	return testSuccess



####################################
#########main program
####################################

#ranges of randomCoords
# randomX (xstart,xstop)
# randomY (ystart,ystop)
xstart=imageSizeX*0.05
print xstart
xstop=imageSizeX*0.95
print xstop

ystart=imageSizeY*0.05
print ystart
ystop=imageSizeX*0.95
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


	testSuccess=False
	while not testSuccess:
		indexList = []
		SVGobj=loadSVGandGetXML(SVGInput_FileName)
		#print "SVGobj:",SVGobj

		d_List=getPathD_asList(SVGobj)
		#print "d_List:",d_List

		#normalizeSVG(d_List)

		numCoords=getNumberOfCoords(d_List)
		print "numCoords:",numCoords

		#pointsMustBeInQuadrants=PercentPointsInQuadrants*numCoords
		print "pointsMustBeInQuadrants:",pointsMustBeInQuadrants

		numSubstitutions=int(numCoords*substitutionPercent)
		print "numSubstitutions:",numSubstitutions
		if numSubstitutions == 0:
			print "The number of points to be replaced is too small, please change the \"numSubstitutions\" parameter."
		else:
			for coordNum in range(0,numSubstitutions):
				
				randIndex=getRandomIndex(numCoords)
				#print "randIndex",coordNum,": ",randIndex

				#idea: test if Coords differnt enough from other images
				##newCoordsOK=false
				## do{
				##	randCoords=getRandomCoords()
				##	newCoordsOK=validateCoords(randCoords)		#concate Coords later?
				##	}while(newCoordsOK==true)

				
				randCoords=getRandomCoords()
				print "randCoords",coordNum,":" ,randCoords,"\n"

				#print_d_List(d_List)
				d_List = substituteCoordsAndGet_d_List(d_List,randIndex,randCoords)
				#print_d_List(d_List)

				newPathD = transform_d_List_toPathD_AndGet(d_List)
				#print newPathD

			testSuccess=areaTest(d_List)
			print testSuccess
			if testSuccess:
				modifySVGAndSave(newPathD,SVGobj)
