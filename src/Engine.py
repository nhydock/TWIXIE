from CommandParser import CommandParser
from Scenario import getRoom

_initial_scenario = "Dungeon Cell"	#the first scenario the game should start in

_instance = None	#singleton instance

#command line parser, if running python 2.7 use argparse, else fall-back to optparse
try:
    import argparse
except ImportError:
    import optparse as argparse
	
#get Singleton instance of the engine
def getInstance():
	global _instance
	if _instance is None:
		Engine()
	return _instance
	
#Engine is the main logic container of the game
#it contains all the objects for scenario, global parser,
class Engine:		
	#initializes the engine to starting game position
	def __init__(self):
		self.scenario = None
		
		#message to display to screen
		self.message = None
		
		#global command parser
		#it takes in the engine so then it can handle scenario specific commands
		self.parser = CommandParser(self)
		
		#player object for the user
		#stores their inventory, score, and other things for them
		self.player = Player()
		
		global _instance
		_instance = self
		
		self.startGame()
		
	def startGame(self):
		self.setScenario(_initial_scenario)
	
	#loads data to a previously saved point
	# @param number	the save id that wants to be loaded
	def loadGame(self, number):
		pass
		
	#saves data to the disk for quick recovery in the future
	#save files will contain the time taken so far, when the data was
	# last saved, a point count, inventory, and the current position
	# scenario
	# @param number	the save id that you want to save into
	def saveGame(self, number):
		pass
		
	#sets the current scenario to a new scenario
	# if the scenario ID (file path to the scenario) is the same then
	# it ignores the setting
	# @return true if a new scenario is set
	#		  false if the sceneraio does not change
	def setScenario(self, s):
		if self.scenario is None or str(self.scenario) != s:
			self.scenario = getRoom(s)
			print self.scenario
			#after loading a new room, tell the parser to look at the room
			self.parser.addLetter("look")
			self.parser.execute()	
			return True
		return False
	
	#gets the current scenario from the engine
	# used for rendering the current scene
	def getScenario(self):
		return self.scenario
		
	def getTyped(self):
		return self.parser.getCurrentTypedMessage()
		
	#displaysprint string a message to the screen
	def show(self, string):
		self.message = string
		
	#checks to see if there is currently a message being rendered
	#if there is then typing input is usually disabled
	def isShowingMessage(self):
		if self.message is not None:
			return True
		return False
	
	#gets the message to be printed to the display
	def getMessage(self):
		return self.message
		
	#gets the engine's current player instance
	def getPlayer(self):
		return self.player
		
#a not so special class
#Players contain the player's name and their inventory	
class Player:
	def __init__(self):
		self.name = None	#name of the player
		self.inventory = []	#inventorys are just a list of items
		
	#sets the player's name
	#this should either be called at the beginning of the game on name input
	#or on data loading
	# @param name the name of your player
	def setName(self, name):
		self.name = name
		
	#sets the inventory of the player
	#inventorys hold all the items of the character
	#what each item can do is
	def setInventory(self, i):
		self.inventory = i;
	
	#adds an item to the inventory
	def addItem(self, item):
		if type(item) is str:
			from Item import loadItem
			item = loadItem(item)
		self.inventory.append(item)
		
	#check if the player has the item
	def hasItem(self, item):
		if type(item) is str:
			from Item import loadItem
			item = loadItem(item)
		return item in self.inventory
	
	#removes the item from the inventory
	#this is usually called after an item is used
	#and is no longer required in the story
	def removeItem(self, item):
		if type(item) is str:
			from Item import loadItem
			item = loadItem(item)
		return self.inventory.remove(item)
		
	#gets the entire inventory for looking at a list of what the player has
	def getInventory(self):
		return self.inventory
