from omega import *
from cyclops import *
from math import *
from euclid import *


class PlanetarySystem(object):
	attributeList = []
	viewNode = None
	panelNode = None
	
	fineLevel = 8	#	fine level stays between 0 to 10
	
	orbitScale = 1.0
	radiusScale = 1.0
	speedScale = 1.0
	
	orbitParameter = { 'name' : 'planetName', 'star' : 'hostName', 'orbit': 'semi-MajorAxis[AU]', 'size': 'pl_rade', 'year': 'orbitPeriod[years]', 'day': 'rotationPeriod[days]', 'obliquity': 'rotationTilt[deg]', 'inclination': 'inclination[deg]' }
	index = {}
	
	def __init__(self):
		self.starList = []
		self.planetList = []
		self.totalDiameter = 0
		self.sphereScaleNode = SceneNode.create(str(id(self)))
		#self.orbitScaleNode = SceneNode.create(id(self))
	@classmethod
	def initialize(cls, str):
		cls.attributeList = str.split(',')
		for key in cls.orbitParameter:
			cls.index.update ( { key: cls.attributeList.index(cls.orbitParameter[key]) } )
		cls.panelNode = SceneNode.create('panelView')
		cls.viewNode = SceneNode.create('mainView')
	def add(self, attrStr):
		attribute = attrStr.split(',')
		if (attribute[0] != attribute[1]):
			self.planetList.append(attribute)
		else:
			self.starList.append(attribute)
	def drawSystem(self):
	
		self.orbitLine = LineSet.create()
		self.orbitLine.setEffect('colored -e green')
		
		for star in self.starList:
			self.drawStar( star )
		for planet in self.planetList:
			self.drawPlanet( planet )
	def drawPlanet(self, planet):
		# Draw orbit
		# Segments # is defined by fineLevel
		#		1 - 36 up to 10 - 360
		if self.fineLevel > 0:
			interval = 10.0 / self.fineLevel
			theta = 0.0
			#radius = float(planet[self.index['orbit']]) * self.orbitScale
			majorAxis = float(planet[self.index['orbit']]) * self.orbitScale
			inclination = float(planet[self.index['inclination']])
			#eccentricity = float(planet[self.index['eccentricity']])
			eccentricity = 0.70
			while theta <= 360:
				radius = majorAxis * (1 - eccentricity*eccentricity) / (1- eccentricity*cos(radians(theta)))
				x = cos(radians(theta)) * cos(radians(inclination)) * radius
				y = sin(radians(theta)) * radius
				z = cos(radians(theta)) * sin(radians(inclination)) * radius
				theta += interval
				nx = cos(radians(theta)) * cos(radians(inclination)) * radius
				ny = sin(radians(theta)) * radius
				nz = cos(radians(theta)) * sin(radians(inclination)) * radius
				line = self.orbitLine.addLine()
				line.setStart (Vector3(x, z, y))
				line.setEnd(Vector3(nx, nz, ny))
	def drawStar(self, star):
		print "Star"
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