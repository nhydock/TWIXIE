'''

2010 Nicholas Hydock
UlDunAd
Ultimate Dungeon Adventure

Licensed under the GNU General Public License V3
     http://www.gnu.org/licenses/gpl.html

'''

from Camera import Camera, DEFAULT_ZOOM
from ImgObj import ImgObj #load in ImgObj to handle resetting clickable buttons when changing scenes

import pygame

import numpy as np
from numpy import float32, array

from OpenGL.GL import *
from OpenGL.GLU import *

from math import *

import Input

INTERNAL_RESOLUTION = [1024.0, 600.0] #resolution at which the engine actually renders at
SOFTWARE = 0	#Basic software rendering mode for pygame
HARDWARE = pygame.OPENGL | pygame.DOUBLEBUF | pygame.HWSURFACE | pygame.HWPALETTE	#Hardware rendering mode for pygame

#basic template of what a scene may contain
class Scene:
    #creation of the scene takes place in here
    # All images, sounds, fonts, and scene specific variables
    # should be initialized here, not later in the process or 
    # as local variables, it should be done HERE!!!
    def __init__(self, engine):
        pass

    #if an image is clicked this should determine what should happen
    def buttonClicked(self, image):
        pass
        
    #if a key is pressed, what happens is controlled in this method
    def keyPressed(self, key, char):
        pass
        
    #anything that is 3d should be rendered in this method
    def render3D(self):
        pass

    #anything that is 2d should be rendered during this process
    def render(self, visibility):
        pass

    #anything involving actions between the user 
    # and the game should happen in here
    def run(self):
        pass
        
#this is the main viewport/engine
#it handles the mouse input, the opengl window
#and which scenes are being rendered.
class Viewport:
    def __init__(self, resolution):
        self.resolution = resolution            #width and height of the viewport
        self.width, self.height = self.resolution
        self.camera = Camera((0, 0), 100)                  
                                                #viewport's opengl camera
        self.scenes = []                        #scenes to render
        self.addScenes = None
        self.input = False                      #is the viewport in its mouse input cycle
        
        self.transitionTime = 32.0             #time it takes to transition between scenes (milliseconds)
        
        self.fade = 0.0

        self.setupViewport()
        
    def setupViewport(self):
        #creates an OpenGL Viewport
        glViewport(0, 0, self.resolution[0], self.resolution[1])

		#enable the lighting and colour materials so things don't show up black
        #glEnable (GL_LIGHTING)
        #glEnable (GL_LIGHT0)
        #glColorMaterial ( GL_FRONT_AND_BACK, GL_AMBIENT_AND_DIFFUSE )
        #glEnable ( GL_COLOR_MATERIAL )
        #glShadeModel(GL_SMOOTH)
        glBlendFunc(GL_SRC_ALPHA,GL_ONE_MINUS_SRC_ALPHA)
        glEnable(GL_BLEND)
        #we clear the buffer to a black colour
        glClearColor(0.0, 0.0, 0.0, 0.0)
        #glClearDepth(1.0)
        #glEnable(GL_DEPTH_TEST)
        glEnable(GL_ALPHA_TEST)
        #glDepthFunc(GL_LEQUAL)
        glHint(GL_PERSPECTIVE_CORRECTION_HINT, GL_NICEST)
        glAlphaFunc(GL_NOTEQUAL,0.0)
		
		#eanble the texturing so all our images and font show up
        glTexEnvf(GL_TEXTURE_ENV, GL_TEXTURE_ENV_MODE, GL_MODULATE)
        glEnable(GL_TEXTURE_2D)
        #glEnable(GL_FOG)
        #glEnable(GL_LIGHTING)
        
    #creates a projection with perspective
    def setPerspectiveProjection(self):
        glMatrixMode( GL_PROJECTION )
        glLoadIdentity()
        glPushMatrix()
        gluPerspective(45, 1.0*self.width/self.height, -500.0, 1000.0)
        
    #creates an orthographic projection
    def setOrthoProjection(self):
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()	#reset the matrix
        glPushMatrix()		#push a new matrix for handling 2D
        
        #create an orthographic display of the windows defined size              
        glOrtho(0, self.width, 0, self.height, -500.0, 1000.0)
        #stretch the internal resolution to the window's resolution
        glScalef((float(self.width)/INTERNAL_RESOLUTION[0]), (float(self.height)/INTERNAL_RESOLUTION[1]), 1.0)
        #pan over to the proper position based on the camera's focus point
        glTranslatef(-self.camera.focusx, -self.camera.focusy, 1.0)
        #zoom in on the scene based on the camera's zoom focus
        glScalef(self.camera.zoom/DEFAULT_ZOOM, self.camera.zoom/DEFAULT_ZOOM, 1.0)
        
    #resets the projection and its matrix so things don't stack from changing projections
    def resetProjection(self):
        glMatrixMode( GL_PROJECTION )
        glPopMatrix()
            
    #changes the topmost scene (the one that is being rendered) with a new one
    def changeScene(self, scene):
        if scene not in self.scenes:
            Input.resetKeyPresses()
            ImgObj.clickableObjs = []
            self.addScene = scene
        else:
            print scene + " is already present"
            
    #removes the passed scene
    def popScene(self, scene):
        if scene in self.scenes:
            Input.resetKeyPresses()
            self.scenes.remove(scene)
        else:
            print scene + " has not been pushed yet"

    #adds the passed scene
    def pushScene(self, scene):
        Input.resetKeyPresses()
        ImgObj.clickableObjs = []
        self.addScene = scene
            
    #checks to see where the position of the mouse is over 
    #an object and if that object has been clicked
    #also handles all the key input and passes it to the current scene
    def detect(self, scene):
        for key, char in Input.getKeyPresses():
            scene.keyPressed(key, char)

        for press in Input.clicks:
            clickedImages = [image.getCollision(press) for image in ImgObj.clickableObjs]
            try:
                x = clickedImages.index(True)
                scene.buttonClicked(ImgObj.clickableObjs[x])
            except ValueError:
                continue


    #renders a scene fully textured
    def render(self, scene, visibility):
        self.setOrthoProjection()           #changes projection so the hud/menus can be drawn
        scene.render(visibility)
        self.resetProjection()
            
    def run(self):
        #clears the buffer
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        #reset matrix every frame
        glLoadIdentity()
        
        #ticks/rate of change in time
        t = 1.0 / self.transitionTime

        if self.addScene:
            self.fade = min(1.0, self.fade + t)
            if self.fade >= 1.0:
                if self.scenes:
                    self.scenes.pop(-1)
                self.scenes.append(self.addScene)
                self.addScene = None
        else:
            self.fade = max(0.0, self.fade - t)                
                
        #fades the screen
        #glColor4f(1,1,1,1-self.fade)
            
        #all scenes should be rendered but not checked for input
        for i, scene in enumerate(self.scenes):
            topmost = bool(scene == self.scenes[-1]) #is the scene the topmost scene
                    
            if topmost:
                scene.run()                         #any calculations of interactions are processed from the
                                                    # previous loop before anything new is rendered

			#run through and render the scene
            try:
				self.render(scene, 1.0)             #renders anything to the scene that is 2D
			#once done rendering the 2D portion, render the 3D
            finally:
                self.setPerspectiveProjection()     #resets the projection to have perspective
                scene.render3D()                    #for anything in the scene that might need perspective
                self.resetProjection()
                
        pygame.display.flip()                       #switches back buffer to the front
            
        if self.scenes:
            #only the topmost scene should be checked for input
            self.detect(self.scenes[-1])            #checks to see if any object on the back buffer has been clicked
            
