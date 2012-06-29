#Base structure for a command
#Commands can be loaded in from a file
#While there are global commands, most commands are defined per room/scenario
class Command(object):
	def __init__(self, name, file = None, node = None):
		#if a file is provided to load data from, use it
		if file is not None:
			loadFromFile(file, node)
		else:
			self.location = None
			self.name = name
		
	#loads a command and definitions from a file
	def loadFromFile(self, file, node):
		pass
		
	def execute(self, s):
		pass
			
	def usable(self):
		#ignore execution if the location where the command can be executed is not equal
		# to the name of the current scenario
		if self.location is not None and Engine.getInstance().getCurrentScenario() is not self.location:
			return False
		return True
		
		
	#sets the location of where commands can be used
	#if None or "Any" is passed through, the command will be usable globally
	def setLocation(self, location):
		if location is "Any":
			location = None
		self.location = location

#command displays the information about the current scenario
class Look(Command):
	def __init__(self):
		super(Look, self).__init__("look")
		self.location = None	#can be used anywhere
		
	#reshows the current rooms message and commands
	def execute(self, s):
		self.engine.show(Engine.getInstance().getCurrentScenario().getMessage())
			
#Command to look at a specific thing in the room or in your inventory
class LookAt(Command):
	def __init__(self):
		super(LookAt, self).__init__("look at")
		self.location = None
	
	#looks at an item
	def execute(self, s):
		#now we look for an item in the list of known items
		#the we look at the items in the scene
		for i in Engine.getInstance().getCurrentScenario().getObjects():
			if s.contains(i):
				Engine.getInstance().show(i.getMessage())
				return
			
		#then we look it the items in the inventory since that list has potential to be longer
		for i in Engine.getInstance().getInventory():
			if s.contains(i):
				Engine.getInstance().show(i.getMessage())
				return
					
		#if nothing was found display an error
		Engine.getInstance().show("No such thing exists")

#commands accessible by the player anywhere
global_commands = [Look(), LookAt()]
