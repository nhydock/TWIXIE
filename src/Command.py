from lxml import etree
import os
import glob

import Engine
import Input
	
#Base structure for a command
#Commands can be loaded in from a file
#While there are global commands, most commands are defined per room/scenario
class Command(object):
	
	
	#commands loaded into the system for use
	#load all the commands in the command folder at startup for caching purposes
	commandCache = []

	def __init__(self, node = None):
		
		self.location = []		#locations acceptable for the use of the command
		self.requirements = []	#items required in inventory before being able to use
		self.consumes = []		#items consumed when the command is used
		self.produces = []		#items produced by the command when used
		self.message = ""		#message shown when the command is executed
		self.name = "blah"		#name of the command, this is the name that you use to invoke the commande
		
		#if a file is provided to load data from, use it
		if node is not None:
			self.loadFromNode(node)
		
		#add self to command cache after being loaded
		Command.commandCache.append(self)
		
	#loads a command and definitions from a file
	def loadFromNode(self, node):
		
		#name of the room	
		self.name = node.attrib["name"]	
		
		#get the description of the room that can be displayed when Look is called
		self.message = node.attrib["message"]
		
		#get all the locations where the command can be used
		self.location = [n.text for n in node.findall("Location")]	
		
		#get all the items required before using
		#required items must be able to be held in the inventory
		requireNode = node.find("Requires")
		self.requirements = [n.attrib["name"] for n in node.findall("Item")]
		
		#get all the items consumed by the command
		#items can either be in the inventory or the environment
		consumeNode = node.find("Consumes")
		self.consumes = [n.attrib["name"] for n in node.findall("Item")]
				
		#get all the items produced by the command
		produceNode = node.find("Produces")
		self.produces = [n.attrib["name"] for n in node.findall("Item")]
		
		#node of all things that are altered by the command
		self.alterNode = node.find("Alter")
		
		print self.message
		print self.location
		print self.requirements
		print self.consumes
		print self.produces
		
	#executes the command itself
	def execute(self, s):
		if self.isUsable():
			#perform altering commands
			self.alter()
			Engine.getInstance().show(self.message)
		else:
			Engine.getInstance().show("You can not do that")
			raise Exception
			
	#checks to see if the command can be used
	def isUsable(self):
		engine = Engine.getInstance()
		#ignore execution if the location where the command can be executed is not equal
		# to the name of the current scenario
		if "any" in self.location or engine.getScenario() in self.location or None in self.location or not self.location:
			print "pass location check"
			if (self.requirements and [engine.getPlayer().hasItem(item) for item in self.requirements]) or not self.requirements:
				print "pass requirements check"
				return True
		print "failed"
		return False
			
	#make changes to the system
	def alter(self):
		#if alternode exists
		if self.alterNode:
			engine = Engine.getInstance()	#the engine of the game
			player = engine.getPlayer()		#the player
			
			#first we look at things on the player to alter
			alterPlayer = alterNode.find("Player")
			
			#we remove things
			removeNode = alterPlayer.find("Remove")
			removeItems = [n.attrib["name"] for n in removeNode.findall("Item")]
	
			#we check the player's inventory to make sure they have all the things necessary
			for item in removeItems:
				if not player.hasItem(item):
					return
	
			#we create items that the player automatically possesses
			createNode = alterPlayer.find("Create")
			createItems = [n.attrib["name"] for n in createNode.findall("Item")]
			
			#if we've made it through everything then we can process it all
			for item in removeItems:
				player.removeItem(item)
				
			for item in createItems:
				player.addItem(item)
			
			#now we look for rooms
			for room in alterNode.findall("Room"):
				#remove various things
				#for rooms you can also remove commands and paths
				removeNode = room.find("Remove")
				removeItems = [n.attrib["name"] for n in removeNode.findall("Item")]
				removeCommands = [n.attrib["name"] for n in removeNode.findall("Command")]
				removePaths = [n.attrib["name"] for n in removeNode.findall("Path")]
				
				#create various things
				createNode = room.find("Create")
				createItems = [n.attrib["name"] for n in createNode.findall("Item")]
				createCommands = [n.attrib["name"] for n in createNode.findall("Command")]
				createPaths = [n.attrib["name"] for n in createNode.findall("Path")]
				
				#if no name is specified, then use the current room as default
				if room.attrib["name"] == None:
					scene = engine.getScenario()	#the current room the player is in
				else
					scene = Scenario.getRoom(room.attrib["name"])
		
				scene.objects -= removeItems	#remove items from list of objects in the room
				scene.objects += createItems	#add new items to the room
				scene.commands -= removeCommands#remove commands
				scene.commands += createCommands#add new commands
				scene.paths -= removePaths		#remove paths
				scene.paths += createPaths		#add paths to take
				
				print scene.objects
				print scene.commands
				print scene.paths
		
	#adds a location of where commands can be used
	#if None or "Any" is passed through, the command will be usable globally
	def setLocation(self, location):
		if location not in self.location:
			self.location.append(location)

	#string representation of the command as how it's acceptable from a command input perspective
	def __str__(self):
		return self.name.lower()
		
	def __repr__(self):
		return self.__str__()

		
#command displays the information about the current scenario
class Look(Command):
	def __init__(self):
		super(Look, self).__init__()
		self.name = "Look"
		self.location = [None]	#can be used anywhere
		
	#reshows the current rooms message and commands
	def execute(self, s):
		s = Engine.getInstance().getScenario().getMessage()
		Engine.getInstance().show(s)
			
#Command to look at a specific thing in the room or in your inventory
class LookAt(Command):
	def __init__(self):
		super(LookAt, self).__init__()
		self.name = "look at"
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

#command to end the game and quit
class Exit(Command):
	def __init__(self):
		super(Exit, self).__init__()
		self.name = "exit"
		self.location = [None]
		
	def execute(self, s):
		Input.finished = True	#sets input to finished, which kills the main game loop
		
#command to pick up an item in the room
class PickUp(Command):
	def __init__(self):
		super(PickUp, self).__init__()
		self.name = "pick up"
		self.location = [None]
		
	def execute(self, s):
		engine = Engine.getInstance()
		itemsInRoom = Engine.getScenario().getObjects()	#get all the items in the room
		
		#search for an item specified
		for item in itemsInRoom:
			if str(item) in s:
				#add the item to the player's inventory if it can be possessed
				if item.possess:
					engine.getPlayer().addItem(item)
				#display an error if the item can not be possessed
				else:
					engine.show("You can not pick up that item")	
				return	
				
#command to go down a path and advance to another location
class Goto(Command):
	def __init__(self):
		super(PickUp, self).__init__()
		self.name = "go to"
		self.location = [None]
		
	def execute(self, s):
		engine = Engine.getInstance()
		availablePaths = Engine.getScenario().getPaths()	#paths that can currently be taken
		
		#search for an item specified
		for path in availablePaths:
			if path in s:
				engine.setScenario(path)
				return	
				
		engine.show("No such path exists")

#commands accessible by the player anywhere
global_commands = [LookAt(), Look(), Exit(), PickUp(), Goto()]

#get all the commands found in the commands folder for caching
for file in glob.glob(os.path.join("..", "data", "commands", "*.xml")):
	Command(etree.parse(file).getroot())

#gets a command by its name if it's already been loaded
def getCommand(name):
	name = name.lower()	#make sure it's in the right case
	print name
	for i, n in enumerate(Command.commandCache):
		print n
		if name == str(n):
			return n
	return None
