
"""
Scenes are abstracted processors that can add a bit more
structure to your SFML application, or any app at that.

Think of scenes as a full system managed state machine.
"""
class Scene(object):

	"""
	Called to perform any kind of preparation work when the
	scene is to be swapped in by a manager.

	As this is a managed process, there really is no need to
	call it before setting it as the currently running scene
	unless you are not using a manager to actually run and 
	render.
	"""
	def start(self):
		return True

	"""
	Called to perform any kind of processing when the scene is
	to be swapped out of a manager.

	Shouldn't be called at any time other than when the system
	is actually done with the scene.  Forcefully calling end()
	may break things
	"""
	def end(self):
		return True

	"""
	Updates any of the scene's logic.  Good for handling 
	manipulation of any of your model's data, such as a game 
	scaled clock, positioning, you name it.  The sfml timer 
	delta is passed down and can be quickly accessed using the 
	delta variable.
	"""
	def update(self, delta):
		pass

	"""
	Draws the scene's objects to the window.  With the timer 
	resolution also passed in, it's also possible to perform
	animation updates during this phase as well
	"""
	def render(self, delta):
		pass

	"""
	Handles key input
	"""
	def key_pressed(self, code):
		pass

	def key_released(self, code):
		pass