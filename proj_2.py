from omega import *
from cyclops import *

class PlanetarySystem(object):
	attributeList = []
	viewNode = None
	panelNode = None
	
	fineLevel = 7 		#	fine level stays between 0 to 10
	
	orbitScale = 1
	radiusScale = 1
	speedScale = 1
	
	orbitParameter = {	'r': 
	
	def __init__(self):
		self.starList = []
		self.planetList = []
	@classmethod
	def initialize(cls, str):
		cls.attributeList = str.split(',')
		cls.viewNode = SceneNode.create('mainView')
		cls.panelNode = SceneNode.create('panelView')
	def add(self, attrStr):
		attribute = attrStr.split(',')
		if (attribute[0] != attribute[1]):
			self.planetList.append(attribute)
		else:
			self.planetList.append(attribute)
		
	def drawSystem(self):
		
	def drawPlanet(thing):
	
	def drawStarI(thing):

def readPlanetarySystemFile(filename, dir = None):
	if ( dir != None ):
		filename = dir + filename
	f = open(filename)
	file = [line.rstrip('\n') for line in f]
	ret = {}
	for line in file:
		ret.update( { line: PlanetarySystem() } )
	return ret

def readPlanetsFile(planetarySystemList, filename, dir = None):
	if ( dir != None ):
		filename = dir + filename
	f = open(filename)
	file = [line.rstrip('\n') for line in f]
	firstLine = True
	for line in file:
		if firstLine == True:
			firstLine = False
			PlanetarySystem.initialize(line)
		elif line[0] != '#':
			attribute = line.partition(',')
			planetarySystemList[attribute[0]].add(line)
			
def drawPlanetarySystems(planetarySystemList):
	for pSys in planetarySystemList:
		planetarySystemList[pSys].drawSystem()