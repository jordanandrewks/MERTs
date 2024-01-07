MENG Final Year project - University of Birmingham, Department of Electrical and Electronic Engineering 
Project Runtime:      10/2018 - 08/2019
Creator/Developer:    Jordan Andrew (Kelly) Small - 1561404
Project Supervisor:   Robert Stone
Title:                Medical Emergency Response Teams (MERT) - Desktop Application & Arduino script
Languages:            Python (Backend) and Kivy (Frontend) | Arduino C/C++ Control


Files in this folder:

- Arduino_BLE (folder)
	- Arduino_BLE.ino (file)

- Desktop App (folder)
	- icons8-heart-with-pulse-filled-100 (2).png (file)
	- main.kv (file)
	- MERTsMain.py (file)
	- JND_Trials.xlsx (file)


README:

The Pulse simulator file has ONLY been tested on a macintosh, running MacOS Mojave. The version number shouldn't be an issue, but you MUST have at least python 3.7.1 - as this is what it was built with. 

TL;DR: Install the following below to get pulseSim working (hasn't been tested on windows): 

You can install this from:
https://www.python.org/downloads/ 

The GUI (graphical user interface) is powered by a Kivy back-end, and requires AT LEAST Kivy 1.9.1
You will NEED this, this can be installed from:
https://kivy.org/#download


Add-ons for python will have to be installed, this is best done with PIP. 
This is can be installed from: 
https://pip.pypa.io/en/stable/installing/


Then the following ad-ons can be installed using PIP:

PySerial - Bluetooth functionality
https://pypi.org/project/pyserial/



The following two are for the Evaluation Windows. 
The Main program and functionality of the Pulse sim should still work without them:
 
xlrd - Reading Values from Excel Sheets | Used for evaluation tools
https://pypi.org/project/xlrd/ 

xlwt - Writing to Excel Sheets | Used for evaluation tools]
https://pypi.org/project/xlwt/ 

NOTE: If any errors regarding missing installation packages, simply 
copy the missing package FLAGGED from the console and search for it. 
It should direct you to Python's add-on website and give you the te-
xt for the command line.


