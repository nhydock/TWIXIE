import CommandParser;
import Scenario;

_initial_scenario = "Start"	#the first scenario the game should start in

#Engine is the main logic container of the game
#it contains all the objects for scenario, global parser,
class Engine:
	_instance = None	#singleton instance
	
	#get Singleton instance of the engine
	@staticmethod
	def get_instance()
		if _instance is None:
			_instance = Engine()
		return _instance
		
	#initializes the engine to starting game position
	def __init__(self):
		#current scenario
		self.scenario = Scenario(_initial_scenario)	
		
		#global command parser
		#it takes in the engine so then it can handle scenario specific commands
		self.parser = CommandParser(self)	
		
	def startGame():
		pass
	
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
		
	#sets the current sceneario to a new scenario
	# if the scenario ID (file path to the scenario) is the same then
	# it ignores the setting
	# @return true if a new scenario is set
	#		  false if the sceneraio does not change
	def setScenario(self, s):
		if (self.scenario.__name__() is not s)
			self.scenario = Scenario(s)
			return true
		return false
	
	
	#displays a message to the screen
	def show(self, string):
		#until we get the graphics implemented, just print the string to the terminal
		print string
		
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
		self.inventory.append(item)
		
	#check if the player has the item
	def hasItem(self, item):
		return self.inventory.count(item) > 0
	
	#removes the item from the inventory
	#this is usually called after an item is used
	#and is no longer required in the story
	def removeItem(self, item):
		return self.inventory.remove(item)
