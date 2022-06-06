# nonogram
A command-line text game to create a nonogram out of an image with a white background. When run, it randomly
selects an image from the `imgs` directory, produces a pixelized image, along with a nonogram puzzle and its
solution in the `results` directory.

## Sample commands to run
- `conda create -n nonogram python=3.9` //to create the virtual environment
- `make install` //to install third-party dependencies from `Makefile`
- `python nonogram.py` //to run the python script
