#!/usr/bin/env python
'''

TWIXIE
Typed-Word Invokable Xenomorphic Incident Engine

@author Nicholas Hydock
@date 2014
@License LGPL v3

This file is part of TWIXIE.

TWIXIE is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

Foobar is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with Foobar.  If not, see <http://www.gnu.org/licenses/>.
'''

import sfml as sf
from Utils.Scene import Manager

FPS = 60
running = True;

"""
Main application Runner
"""
class Runner:
   def __init__(self):
      #prep scenes
      Manager.init()
      Manager.register("test", "Scenes.Test.TestScene");
      Manager.create_and_set("test");

      #initialize the display
      self.window = sf.RenderWindow(sf.VideoMode(640, 480), 'TWIXIE')
      self.window.framerate_limit = FPS

      self.clock = sf.Clock()

   def update(self):
      global running

      for event in self.window.iter_events():
         if event.type == sf.Event.CLOSED:
            running = False
         if event.type == sf.Event.TEXT_ENTERED or \
            event.type == sf.Event.KEY_PRESSED or \
            event.type == sf.Event.KEY_RELEASED:
            Manager.handle_input(event)

      #get the amount of time passed since the last update
      delta = self.clock.elapsed_time.as_seconds()
      self.clock.restart()

      #process the manager
      Manager.update(delta)

      #clear the buffer
      self.window.clear(sf.Color.WHITE)

      Manager.render(self.window, delta)

      #flush to the display
      self.window.display()


   def destroy(self):
      self.window.close()
      Manager.destroy()

def main():
   global running

   app = Runner()

   while running:
      app.update()
        
   app.destroy()


if __name__ == '__main__':
    main()