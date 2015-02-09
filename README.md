# Breakout
[Breakout](http://en.wikipedia.org/wiki/Breakout_%28video_game%29) game engine implemented in Python, [PyGame](http://pygame.org/) and OpenGL.

I've recorded a video of this game running. You can watch it [here](https://vimeo.com/118087355).

Scroll-down for screenshots.

# Requirements

- Python 2.7 or above (does not support Python 3.x)
- Ubuntu or Mac OS X
- PyGame
- PyOpenGL
- PyTest (to run automated unit tests)
- Enum34 (Python 3.4 enum support backported to 2.7)

## Ubuntu Linux Setup

(Tested on Ubuntu 10.04 and 10.10)

     sudo apt-get install python-opengl
     sudo apt-get install python-pygame
     sudo apt-get install python-setuptools
     pip install enum34
     
## Mac OS X Setup

(Tested on Mac OS X 10.10 Yosemite)

You need to have [Homebrew](http://brew.sh) and [Python 2.7](http://docs.python-guide.org/en/latest/starting/install/osx/) properly installed.

    brew install Caskroom/cask/xquartz
    brew install pygame
    pip install pyopengl
    pip install enum34
     
# Running the Game

Enter the 'source' directory and execute script 'run.sh'.

# Running Automated Unit Tests

Make sure you have pytest installed:

    pip install pytest

Then execute inside the 'source' folder:

    py.test

# Screenshots

![Screenshot 01](screenshots/01.png)
![Screenshot 02](screenshots/02.png)
![Screenshot 03](screenshots/03.png)
![Screenshot 04](screenshots/04.png)
![Screenshot 05](screenshots/05.png)
