#svgGen 
[A simple program that generates several different SVG files from a source image.]
  
  
###description:
First, the image is replaced with an image in absolute points. 
That is the case, and then capitalize positivize negative relative x and y.

Then the image is normalized in my sense. 
Can now be generated from the normalized image a set number of images, just by replacing a fixed percentage of points by random points.



required: library svgfig https://code.google.com/p/svgfig/

Download the latest version, extract it, go in the svgfig folder and install it with (on a Debian-based Linux):

	sudo python setup.py install

Then they make the program executable, adjust the parameters in the header of the source code and run it:

	sudo chmod +x svgGen.py
	./svgGen.py