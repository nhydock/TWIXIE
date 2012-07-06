from lxml import etree
from Command import Command, loadCommand
import os
from TwiObj import TwiObj
import glob

#Room object
#Rooms are where all the action happens
#They have their own scenario specific commands and items and paths to take
#Rooms can only be defined in room files, they can not be defined in-line like
# how commands and items can be nested within one another
class Scenario(TwiObj):
	cache = []	#already loaded rooms
	
	def __init__(self, node):
		super(Scenario, self).__init__(node.attrib["name"], node.find("Description").text)
		
		self.objects = []	#all the items found in the room
		self.commands = []	#all the names of commands specific to the room
		self.paths = []		#all the available paths for taking
		
		print self.description
		
		#commands can be defined in file or referenced
		self.commands = []
		for n in node.findall("Command"):
			self.commands.append(loadCommand(n))
				
		print self.commands
		
		self.objects = []
		"""
		for n in root.findall("Item"):
			if len(n) > 0: 
				self.commands.append(Item(node = n))
			else: 
				self.commands.append(getCommand(n.attrib["name"]))
		"""
		
		self.paths = [n.attrib["name"] for n in node.findall("Path")]
		
		Scenario.cache.append(self)
		
	#gets a list of objects within the room that
	#can be looked at
	def getObjects(self):
		return self.objects
		
	#gets a list of the different commands
	#that are unique to this scenario
	def getCommands(self):
		return self.commands

	#gets all the paths available to take
	def getPaths(self):
		return paths


#gets a preloaded room
def getRoom(name):
	#don't try loading anything if node is Nonetype
	if name is None:
		return None
		
	name = name.lower() #ensure right casing
	print "Room is search of :" + name
	for room in Scenario.cache:
		print str(room)
		if name == str(room):
			print "found room"
			return room
	print "room not found"
	return None
	
#all rooms are preloaded into the system at start up
for file in glob.glob(os.path.join("..", "data", "rooms", "*.xml")):
	Scenario(etree.parse(file).getroot())
	
print Scenario.cache
