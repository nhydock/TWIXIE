import Engine
import Input

#Base structure for a command
#Commands can be loaded in from a file
#While there are global commands, most commands are defined per room/scenario
class Command(object):
	
	commandCache = []	#commands loaded into the system for use
	
	def __init__(self, name, file = None, node = None):
		
		self.location = []		#locations acceptable for the use of the command
		self.requirements = []	#items required in inventory before being able to use
		self.consumes = []		#items consumed when the command is used
		self.produces = []		#items produced by the command when used
		self.message = ""		#message shown when the command is executed
		self.name = name		#name of the command, this is the name that you use to invoke the commande
		
		#if a file is provided to load data from, use it
		if file is not None:
			loadFromFile(file, node)
		
		#add self to command cache after being loaded
		Command.commandCache.append(self)
		print self
		
	#loads a command and definitions from a file
	def loadFromFile(self, file, node = None):
		if node is not None:
			dom = node
		else:
			source = open(os.path.join("..", "data", "commands", path + ".xml"))
			dom = parse(source)
		
		#root of the xml
		top = dom.getElementsByTagName("Command")[0]
		
		#name of the room	
		self.name = top.getElementsByTagName("Name")[0].firstChild.data	
		
		#get the description of the room that can be displayed when Look is called
		self.message = top.getElementsByTagName("Message")[0].firstChild.data
		
		#get all the locations where the command can be used
		self.location = [n.firstChild.data for n in top.getElementsByTagName("Location")]	
		
		#get all the items required before using
		self.requirements = [n.firstChild.data for n in top.getElementsByTagName("RequireItem")]
		
		#get all the items consumed by the command
		#items can either be in the inventory or the environment
		self.consumes = [n.firstChild.data for n in top.getElementsByTagName("ConsumesItem")]
		#just in case, all consumed items are also added to the list of requirements
		for item in self.consumes:
			if item not in self.requirements:
				self.requirements.append(item)
				
		#get all the items produced by the command
		self.produces = [n.firstChild.data for n in top.getElementsByTagName("ProducesItem")]
		
	#executes the command itself
	def execute(self, s):
		if self.isUsable():
			#consume the items first
			self.consumeItems()
			#then produce new items
			self.produceItems()
			#show the message to screen
			Engine.getInstance().show(self.message)
			
	#checks to see if the command can be used
	def isUsable(self):
		engine = Engine.getInstance()
		#ignore execution if the location where the command can be executed is not equal
		# to the name of the current scenario
		if "any" in self.location or engine.getScenario() in self.location or None in self.location:
			if (self.requirements and [engine.getPlayer().hasItem(item) for item in self.requirements]) or not self.requirements:
				return True
		return False
	
	#consumes an item so it may no longer be used
	def consumeItem(self):
		#first get the engine to work with
		engine = Engine.getInstance()
		
		for item in self.consumes:
			#first check the player's inventory for the item
			player = engine.getPlayer()
			if player.remove(item):
				continue
			
			#check the environment for the item to possibly be there and not in the inventory
			scenario = engine.getScenario()
			if not player.remove(item):
				raise Exception("You can perform such a command, you do not have enough items")
				
	#adds a location of where commands can be used
	#if None or "Any" is passed through, the command will be usable globally
	def setLocation(self, location):
		if location not in self.location:
			self.location.append(location)

	def __str__(self):
		return self.name
		
#command displays the information about the current scenario
class Look(Command):
	def __init__(self):
		super(Look, self).__init__("look")
		self.location = [None]	#can be used anywhere
		
	#reshows the current rooms message and commands
	def execute(self, s):
		s = Engine.getInstance().getScenario().getMessage()
		Engine.getInstance().show(s)
			
#Command to look at a specific thing in the room or in your inventory
class LookAt(Command):
	def __init__(self):
		super(LookAt, self).__init__("look at")
		self.location = [None]
	
	#looks at an item
	def execute(self, s):
		#now we look for an item in the list of known items
		#first we look at the items in the scene because that list will most likely be smaller than the inventory
		for i in Engine.getInstance().getScenario().getObjects():
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

class Exit(Command):
	def __init__(self):
		super(Exit, self).__init__("exit")
		self.location = [None]
		
	def execute(self, s):
		Input.finished = True

#commands accessible by the player anywhere
global_commands = [Look(), LookAt(), Exit()]
