#genRandSVG

python script to generate randomized SVG images.

## why?

Randomized images are useful for cognitive tests. Test persons have to remember images without associations.
If you don't have an association to an image, it is more difficult to recognize the image. So the brain acitivity of real "remembering" can be determined.

## installation

- install python-pip on your os, e.g (Ubuntu/Arch Linux).:

`sudo apt-get install python-pip` or `sudo pacamn -S python-pip`

- install svgwrite with pip e.g.:

`sudo pip install svgwrite`


## usage

`python genRandSVG.py --n 15 --s 1280 1024 --el 4 --d 100 --a 15`

### explanation

The program call generates 15 images with a size of 1280 width and 1024 height. The image includes 4 SVG elements (like a line, a cubic bezier or something like this) which should have at least a distance of 100 pixel with each other. The generator has 15 attempts to get a new point with a valid distance to previous points.

### example output

![ScreenShot](https://raw.githubusercontent.com/ReneMuhl/genRandSVG/master/genRandSVG/meta/example_output.png)


## help

```
usage: genRandSVG.py [-h] --n [N] --s width height [--el [EL]] [--d [D]]
                     [--a [A]]

optional arguments:
  -h, --help            show this help message and exit
  --n [N], --number [N]
                        Integer specifies the number of images.
  --s width height, --size width height
                        Integer specifies the width and height of the images.
  --el [EL], --elements [EL]
                        Integer specifies the number of elements that should
                        be created.
                        elements < 4 => simple SVG
                        elements < 10 => moderate SVG
                        elements >= 10 => complex SVG
  --d [D], --distance [D]
                        Integer specifies the distance between the new points
                        and all previous points.
  --a [A], --attempts [A]
                        Integer specifies the number of attempt to get a new
                        point with correct distance to all previous points.

```

#### errors, comments and suggestions: Mail@ReneM{dot}github{at}gmail{dot}com
