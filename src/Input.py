'''

2012 Nicholas Hydock
TWIXIE

Licensed under the GNU General Public License V3
     http://www.gnu.org/licenses/gpl.html

'''
from threading import Thread
import pygame
from pygame.locals import *

#input handling
mousepos = (0, 0)       #mouse position
clicks = []             #clicks this frame
keypresses = []         #key presses this frame

#tracks if the game engine is finished
finished = False

#input keys
KillButton = K_ESCAPE

#adds a key press to the list of key presses
def processKeyPress(press):
	keypresses.append((press.key, press.unicode))

#get the keys pressed, one by one
def getKeyPresses():
	while len(keypresses):
		yield keypresses.pop(0)

#clear the key pressed list
def resetKeyPresses():
	keypresses[:] = []

#resets the input handler
def reset():
	resetKeyPresses()
	
#run thread
def update():
	global finished
	while not finished:
		event = pygame.event.poll()	#get input events
		if event.type == NOEVENT:
			break  # no more events this frame
		elif event.type == QUIT:
			finished = True
			break
		elif event.type == KEYDOWN:
			#end the game if kill key is pressed
			if event.key == KillButton:
				finished = True
				break
			
			processKeyPress(event)
