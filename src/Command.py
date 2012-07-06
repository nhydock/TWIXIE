from lxml import etree
import os
import glob

import Engine
import Input
from TwiObj import TwiObj
	
#Base structure for a command
#Commands can be loaded in from a file
#While there are global commands, most commands are defined per room/scenario
class Command(TwiObj):
	
	#commands loaded into the system for use
	#load all the commands in the command folder at startup for caching purposes
	cache = []

	def __init__(self, node):
		super(Command, self).__init__(node.attrib["name"], node.find("Message").text)
		
		self.requirements = []	#items required in inventory before being able to use
		self.consumes = []		#items consumed when the command is used
		self.produces = []		#items produced by the command when used
		
		#get all the items required before using
		#required items must be able to be held in the inventory
		requireNode = node.find("Requires")
		self.requirements = []
		if requireNode is not None:
			for n in requireNode.findall("Item"):
				self.requirements.append(n.attrib["name"].lower())
		
		#node of all things that are altered by the command
		self.alterNode = node.find("Alter")
		#if alternode exists
		if self.alterNode is not None:
			self.alterPlayer = [[],[]]
			#first we look at things on the player to alter
			alterPlayer = self.alterNode.find("Player")
			if alterPlayer is not None:
				#we remove things
				#we don't need item objects for removing items, we just need their names since you can only remove references
				removeNode = alterPlayer.find("Remove")
				if removeNode is not None:
					self.alterPlayer[0] = [n.attrib["name"].lower() for n in removeNode.findall("Item")]
					self.requirements += self.alterPlayer[0]	#add all items that are removed from the player to the list of requirements
		
				#we create items that the player automatically possesses
				#in the case of adding items, we need to actually have an item instance added
				createNode = alterPlayer.find("Create")
				if createNode is not None:
					self.alterPlayer[1] = [n.attrib["name"].lower() for n in createNode.findall("Item")]
			
			self.alterRooms = {}
			#represent rooms in a map
			#name of the room is equal to a list of all things removed
			#now we look for rooms
			for room in self.alterNode.findall("Room"):
				try:
					roomName = room.attrib["name"]
					self.alterRooms[roomName] = [[[],[]],[[],[]],[[],[]]]
				except KeyError:
					roomName = None
					self.alterRooms[roomName] = [[[],[]],[[],[]],[[],[]]]
				print roomName
				
				#remove various things
				#for rooms you can also remove commands and paths
				removeNode = room.find("Remove")
				if removeNode is not None:
					#remove items
					for n in removeNode.findall("Item"):
						self.alterRooms[roomName][0][0].append(n)
					#remove commands
					for n in removeNode.findall("Command"):
						self.alterRooms[roomName][1][0].append(n)
					#remove paths
					for n in removeNode.findall("Path"):
						self.alterRooms[roomName][2][0].append(n.attrib["name"])
				
				#create various things
				createNode = room.find("Create")
				print createNode
				if createNode is not None:
					#add items
					for n in createNode.findall("Item"):
						self.alterRooms[roomName][0][1].append(n)
					#remove commands
					for n in createNode.findall("Command"):
						self.alterRooms[roomName][1][1].append(n)
					#remove paths
					for n in createNode.findall("Path"):
						self.alterRooms[roomName][2][1].append(n.attrib["name"])
				
				print self.alterRooms[roomName]
				
		print self.description
		print self.requirements
		
		#add self to command cache after being loaded
		Command.cache.append(self)

	#executes the command itself
	def execute(self, s):
		if self.isUsable():
			#perform altering commands
			self.alter()
			Engine.getInstance().show(self.description)
		else:
			Engine.getInstance().show("You can not do that")
			raise Exception
			
	#checks to see if the command can be used
	def isUsable(self):
		engine = Engine.getInstance()
		#ignore execution if the location where the command can be executed is not equal
		# to the name of the current scenario
		if not self.requirements:
			print "no requirements, automatically pass"
			return True
		
		for item in self.requirements:
			if not engine.getPlayer().hasItem(item):
				print "failed, did not have " + item
				return False
		print "pass requirements check"
		return True
			
	#make changes to the system
	def alter(self):
		engine = Engine.getInstance()	#the engine of the game
		player = engine.getPlayer()		#the player
			
		#load these up now so there isn't a recursion error earlier on
		from Item import loadItem		
		from Scenario import getRoom
			
		#go through the list of items to remove from the player
		for item in self.alterPlayer[0]:
			player.removeItem(loadItem(item))
					
		#go through the list of items to add to the player
		for item in self.alterPlayer[1]:
			player.addItem(loadItem(item))
			
		#go through the list of rooms to be altered
		for room in self.alterRooms.keys():
			if room is not None:
				scene = getRoom(room)
			else:
				scene = engine.getScenario()
				
			#remove things from the rooms
			for n in self.alterRooms[room][0][0]:
				scene.objects.remove(loadItem(n))
			for n in self.alterRooms[room][1][0]:
				scene.commands.remove(loadCommand(n))
			for n in self.alterRooms[room][2][0]:
				scene.paths.remove(getRoom(n))
			#add things to the rooms
			for n in self.alterRooms[room][0][1]:
				scene.objects.append(loadItem(n))
			for n in self.alterRooms[room][1][1]:
				scene.commands.append(loadCommand(n))
			for n in self.alterRooms[room][2][1]:
				scene.paths.append(getRoom(n))
							
			print scene.objects
			print scene.commands
			print scene.paths
		
#command displays the information about the current scenario
class Look(Command):
	def __init__(self):
		self.name = "Look"
		self.location = [None]	#can be used anywhere
		
	#reshows the current rooms message and commands
	def execute(self, s):
		s = Engine.getInstance().getScenario().getDescription()
		Engine.getInstance().show(s)
			
#Command to look at a specific thing in the room or in your inventory
class LookAt(Command):
	def __init__(self):
		self.name = "look at"
		self.location = [None]
	
	#looks at an item
	def execute(self, s):
		#now we look for an item in the list of known items
		for i in Engine.getInstance().getScenario().getObjects()+Engine.getInstance().getPlayer().getInventory():
			if str(i) in s:
				Engine.getInstance().show(i.getDescription())
				return
					
		#if nothing was found display an error
		Engine.getInstance().show("No such thing exists")

#command to end the game and quit
class Exit(Command):
	def __init__(self):
		self.name = "exit"
		self.location = [None]
		
	def execute(self, s):
		Input.finished = True	#sets input to finished, which kills the main game loop
		
#command to pick up an item in the room
class PickUp(Command):
	def __init__(self):
		self.name = "pick up"
		self.location = [None]
		
	def execute(self, s):
		engine = Engine.getInstance()
		itemsInRoom = engine.getScenario().getObjects()	#get all the items in the room
		
		#search for an item specified
		for item in itemsInRoom:
			if str(item) in s:
				#add the item to the player's inventory if it can be possessed
				if item.possess:
					engine.getPlayer().addItem(item)
					itemsInRoom.remove(item)	#remove the item from the room after placing it in your inventory
					engine.show("You picked up the " + str(item))
				#display an error if the item can not be possessed
				else:
					engine.show("You can not pick up that item")	
				return	
				
#command to go down a path and advance to another location
class Goto(Command):
	def __init__(self):
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

#gets a command by its name if it's already been loaded
def loadCommand(node):
	#don't try loading anything if node is Nonetype
	if node is None:
		return None
		
	#if a node with more than just the name attribute defined, then load a new command
	if len(node) > 0 and type(node) is not str:
		return Command(node)
	#else retrieve one that has already been created by its name 
	else:
		if type(node) is not str:
			name = node.attrib["name"].lower()
		else:
			name = node.lower()
		for n in Command.cache:
			if name == str(n):
				return n
		return None	
	

#get all the commands found in the commands folder for caching
for file in glob.glob(os.path.join("..", "data", "commands", "*.xml")):
	loadCommand(etree.parse(file).getroot())

print Command.cache
