#!/usr/bin/python
# -*- coding: utf-8 -*-

# 2do:
	#test with plain and inkscape SVG
	#conventions variablenames
	# distinguish between width and height (different maxima)
	# combine the two for loops, roll the dice for index later
	## if the el.isalpha == true -> roll the dice again
	# create structure with methods, commandline arguments like input, number
	## of SVGs to be generated



import svgfig  		#parse SVG
import random 		#random numbers gen
#import re 			#regex
#import copy		#copy Objects

####################################
#########params
####################################

SVGInput_FileName="plainSVG1.svg"
SVGOutput_FileNameTemplate="genSVG"
numImages=5
substitutionPercent=0.6					#specifies how many Coord be replaced

####################################
#########functions
####################################

def loadSVGandGetXML(filename):
	#test if file exists
	SVGobj = svgfig.load(filename)
	return SVGobj


def getPathD_asList(SVGobj):
	SVGpathD=SVGobj[2,0,u'd']
	#print SVGpathD,"\n"
	d_List = SVGpathD.split()	#split() returns a list of esments
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
	randIndex=random.randint(0,numCoords)
	return randIndex


def getRandomCoords():
	#start and stop has a connection to width and height
	# get two random coordinates 
	# up to now with fixed range
	start=-500
	stop=500
	rand1=random.uniform(start,stop)
	rand2=random.uniform(start,stop)
	#validate coords with a seperate function/strategy
	#print "rand1 rand2: ", rand1, rand2, "\n"
	randCoords=str(rand1) + "," + str(rand2)
	return randCoords


def print_d_List(d_List):
	for index in range(0,len(d_List)):
		print "dlist[",index,"]: ",d_List[index],"\n"

 		
def substituteCoordsAndGet_d_List(d_List,randIndex,randCoords):			#call by value or call by reference?
	numCoords=0
	for index in range(0,len(d_List)):
		#print d_List[index][0].isalpha()
		if not d_List[index][0].isalpha():
			#print el, "\n"
			numCoords+=1
			if numCoords == randIndex:
				print "=========>",d_List[index], "\n"
				d_List[index]=randCoords
				print "===============>",d_List[index], "\n"
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


def modifySVGAndSave(newPathD,SVGobj,currentImg):
	SVGobj[2,0,u'd']=newPathD
	outputFileName=SVGOutput_FileNameTemplate+str(currentImg)+".svg"
	print outputFileName
	SVGobj.save(outputFileName)


####################################
#########main program
####################################

SVGobj=loadSVGandGetXML(SVGInput_FileName)
#print "SVGobj:",SVGobj

d_List=getPathD_asList(SVGobj)
#print "d_List:",d_List

numCoords=getNumberOfCoords(d_List)
print "numCoords:",numCoords


numSubstitutions=int(numCoords*substitutionPercent)
print "numSubstitutions:",numSubstitutions


for currentImg in range(0,numImages):	
	for coordNum in range(0,numSubstitutions):
		randIndex=getRandomIndex(numCoords)
		print "randIndex",coordNum,": ",randIndex


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

	modifySVGAndSave(newPathD,SVGobj,currentImg)

