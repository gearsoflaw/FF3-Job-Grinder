# FF3 Job Grinder
A naive application that can do some rudimentary grinding to level up Jobs in Final Fantasy 3 (Steam)

# Getting Started
## Required Python Modules
* OpenCv
..* https://pypi.org/project/opencv-python/
* numpy
..* https://pypi.org/project/numpy/1.12.0/
* pywin32
..* https://www.lfd.uci.edu/~gohlke/pythonlibs/#pywin32

## Constraints
* This solution is only supported on windows due to the implementation of grabscreen.py

# How to use this tool
## Configure game settings
* Resolution: 800x600 @ 60Hz
* Fullscreen: Must be unticked
![FF3-Settings Example](../media/ff3-settings.jpg?raw=true)

## Position Screen
* Place the screen in the top left of the screen
![FF3-Screen-Position Example](../media/ff3-screen-position.jpg?raw=true)

### Hint
It is important to place the window correctly to ensure that when the application is reading in the images it can see the game.
* In `ff3_consts_running.py` you can set `SHOW_SCREEN` to `True`, this will draw a window showing you exactly what the application is seeing, this window needs to be a mirror of what is happening in the game window.

## Best place to Grind
In the forest just south of Ur.

### Hint
Make sure you place all characters in the backrow to minimize the damage they take.

## Configure for the party that is active
Inside `ff3_consts_running.py` there are many different settings you can tweak and play with, however, the settings that will be most useful is setting up the commands to perform based on the characters that are active.

i.e. a Thief does not have a Guard command, which means a Thief needs to perform the Steal command instead.
For example: If you were to have Arc in character position 2 and he was a Thief and the other 3 characters were Warriors you would need to setup the `GRIND_CMD` such that the characters 1, 3 and 4 perform the standard grind action `CMD_STD_GRIND` while the character in position 2 is setup for the special steal command `CMD_SP_STEAL`:
* `GRIND_CMD = {CHAR_1: CMD_STD_GRIND, CHAR_2: CMD_SP_STEAL, CHAR_3: CMD_STD_GRIND, CHAR_4: CMD_STD_GRIND}`

You can also alter how many rounds to 'Grind' for before the attack commands get issued by changing the value for `GRIND_ROUNDS` which is set to 6 by default, this means on round 6 the Attack commands will begin.

# Other Helpful Links

## Dowload for Visual Studio Code
https://code.visualstudio.com/download

## Resources if you have not used VS Code for Python
https://code.visualstudio.com/docs/python/python-tutorial

# Why does this even exist?
Upon discovery of the amount of time to legitimately grind to level all Jobs up to Level 99 for all characters for the 'Jack of All Trades' achievement, I initially decided to abandon the achievement, after some reflection I realized the process of grinding is brain numbingly straight forward, and thought of this as a great opportunity to learn Python (This is the first Python code I have ever created).

I personally do not believe in the point of using trainers or cheat engine as tools of convenience to unlock achievements, what I do believe though is to invest the effort to learn a new skill and grow my own skill set as a developer!

So with this tool, I can setup my characters and then run the script while I spend some time doing other more constructive things with my life, without feeling guilty that this could be considered 'cheating'. I have invested the effort to gain real life skills to unlock this convenience.

Creating a trainer may have been considered more efficient to accomplish this, but, it does not fulfil my own desire to learn, taking the first step in understanding image processing and getting input commands to work is simple and gives me a foundation to tackle other challenges in games as well as a precurser to machine learning.

# Acknowledgments
Sentdex: https://pythonprogramming.net/direct-input-game-python-plays-gta-v/
This application effectively automates the process as described here: https://www.ign.com/wikis/final-fantasy-iii/Job_Level_Grinding
