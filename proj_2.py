class PlanetarySystem(object):
	attributeList = []
	def __init__(self):
		self.starList = {}
		self.planetList = []
	@classmethod
	def setAttribute(cls, str):
		cls.attributeList = str.split(',')
	def add(self, attrStr):
		print attrStr
		attrList = attrStr.split(',')
		
	def addStar(self, str):
		print str
	def addPlanet(self, str):
		print attributeList
	def drawSystem(self):
		print "draw it"

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
			PlanetarySystem.setAttribute(line)
		elif line[0] != '#':
			attribute = line.partition(',')
			planetarySystemList[attribute[0]].add(line)
			
		