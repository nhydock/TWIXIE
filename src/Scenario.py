from lxml import etree
from Command import Command, getCommand
import os

class Scenario:
	def __init__(self, path):
		self.name = ""		#name of the room
		self.objects = []	#all the items found in the room
		self.commands = []	#all the names of commands specific to the room
		self.paths = []		#all the available paths for taking
		self.message = ""	#the description of the room that can be displayed when Look is called
		
		#now we do the parsing of the xml file
		source = open(os.path.join("..", "data", "rooms", path + ".xml"))
		tree = etree.parse(source)
		#root of the xml
		root = tree.getroot()
		
		self.name = root.attrib["name"]
		self.message = root.attrib["description"]
		
		#commands can be defined in file or referenced
		self.commands = []
		for n in root.findall("Command"):
			#if no sub nodes, then the 
			if len(n) > 0: 
				self.commands.append(Command(node = n))
			else: 
				self.commands.append(getCommand(n.attrib["name"]))
				
		print self.commands
		
		self.objects = []
		"""
		for n in root.findall("Item"):
			if len(n) > 0: 
				self.commands.append(Item(node = n))
			else: 
				self.commands.append(getCommand(n.attrib["name"]))
		"""
		
		self.paths = [n.attrib["name"] for n in root.findall("Path")]
		
	#gets a list of objects within the room that
	#can be looked at
	def getObjects(self):
		return self.objects
		
	#gets a list of the different commands
	#that are unique to this scenario
	def getCommands(self):
		return self.commands
		
	#gets the room description for displaying on
	#the screen when describing things
	def getMessage(self):
		return self.message

	#gets all the paths available to take
	def getPaths(self):
		return paths

#gets a preloaded room
def getRoom(name):
	for room in Scenario.cache:
		if name == room:
			return room
	return None
