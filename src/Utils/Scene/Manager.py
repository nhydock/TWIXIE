import importlib
import sfml as sf
from threading import Thread

_loading = False

"""
Scene managers help generate new scenes on request as well as maintain
a current visible setup to the game's current scene modules.  Managed 
scenes can be swapped in and out of the manager as long as they are a
type that the manager is capable of managing.

A scene manager is good for adding a layer of abstraction to your game
so you don't have to man-handle all the processes yourself.

For added convenience, a Manager is designed to be run as a singleton
with static methods existing so you can use it as such.  However, this
is Python, so it can be initialized as a standard object and you can
have multiple managers, accessing their \"private\" methods directly
if you so desire.
"""
class Manager(object):
	_instance = None

	"""
	Ready the singleton Manager
	"""
	def init():
		Manager._instance = Manager()

	"""
	Constructs a Scene Manager
	"""
	def __init__(self):
		self.scenes = {}
		self.active = None
		self.next = None

		self._loadThread = None

	"""
	Add a new scene type to be managed and produced
	"""
	def _register(self, name, classname):
		self.scenes[name] = classname

	"""
	Add a new scene type to be managed and produced
	"""
	@staticmethod
	def register(name, classname):
		Manager._instance._register(name, classname)

	"""
	Create a new scene instance by name using reflection.
	This just pumps out a factoried scene, and does not actually manage it.
	Use this if you desire to create a cached scene that you intend on
	swapping in later
	"""
	def _create(self, name):
		module_name = self.scenes[name]
		class_name = module_name.split(".")[-1]
		module_name = ".".join(module_name.split(".")[:-1])

		if module_name:
			module = importlib.import_module(module_name)
			return getattr(module, class_name)()

	"""
	Create a new scene instance by name using reflection.
	This just pumps out a factoried scene, and does not actually manage it.
	Use this if you desire to create a cached scene that you intend on
	swapping in later
	"""
	@staticmethod
	def create(name):
		Manager._instance._create(name)

	"""
	Method for asynchronous threaded loading/swapping of scenes
	"""
	def _load(self):
		global _loading

		_loading = False;
		while not _loading:
			_loading = self.next.start()
			if self.active:
				_loading = _loading and self.active.end()
		#only swap once both the active since is finished decomposing
		# and when the next scene is done preparing
		self.active = None
		self.active = self.next
		self.next = None

	def _set(self, scene):
		if scene:
			self.next = scene
			self._loadThread = Thread(target=self._load)
			self._loadThread.start()

	def set(scene):
		Manager._instance._set(scene)

	"""
	Create a new scene instance by name using reflection.
	This just pumps out a factoried scene, and does not actually manage it.
	Use this if you desire to create a cached scene that you intend on
	swapping in later
	"""
	def _create_and_set(self, name):
		self._set(self._create(name))


	"""
	Create a new scene instance by name using reflection.
	This just pumps out a factoried scene, and does not actually manage it.
	Use this if you desire to create a cached scene that you intend on
	swapping in later
	"""
	@staticmethod
	def create_and_set(name):
		Manager._instance._create_and_set(name)

	"""
	Perform generic management updating
	The game should call this every update cycle as the manager sends down the
	chain of commands.
	"""
	def _update(self, delta):

		if self.next is None:
			#update the currently visible scene
			self.active.update(delta)
		#know to swap out
		else:
			if _loading:
				self._loadThread.join()

	"""
	Perform generic management updating
	The game should call this every update cycle as the manager sends down the
	chain of commands.
	"""
	@staticmethod
	def update(delta):
		Manager._instance._update(delta)

	"""
	Perform generic management updating
	The game should call this every update cycle as the manager sends down the
	chain of commands.
	"""
	def _render(self, context, delta):

		if not self.active:
			return

		if self.next is None:
			self.active.render(context, delta)
		else:
			#draw a loading screen here in the future
			pass

	@staticmethod
	def render(context, delta):
		Manager._instance._render(context, delta)

	"""
	Delegates input events down to the scene.

	While certain kinds of input are more than likely best
	to just be handled in the update method due to always
	being able to fetch the precise state of the keys,
	other kinds of input, such as typing, are simple,
	non-precise scenarios that are best handled through
	using SFML's event system.
	"""
	def _handle_input(self, event):
		if not self.active:
			return

		if event.type == sf.Event.KEY_PRESSED or event.type == sf.Event.TEXT_ENTERED:
			self.active.key_pressed(event)
		elif event.type == sf.Event.KEY_RELEASED:
			self.active.key_released(event)

	@staticmethod
	def handle_input(event):
		Manager._instance._handle_input(event)

	"""
	Kill the manager and it's currently existing scenes
	"""
	def _destroy(self):
		if self._loadThread.isAlive():
			self._loadThread.join()

		if (self.active):
			while not self.active.end(): 
				pass
			self.active = None

		if (self.next):
			while not self.next.end(): 
				pass

			self.next = None

	@staticmethod
	def destroy():
		Manager._instance._destroy()