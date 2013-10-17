from omega import *
from cyclops import *
from math import *
from euclid import *

class PlanetarySystem(object):
	fineLevel = 8	#	fine level stays between 0 to 10
	orbitScale = 1.0
	radiusScale = 1.0
	speedScale = 1.0
	ratio = 10.0
	lineThickness = 0.02

	def __init__(self, star, planets):
		self.starList = star
		self.planetList = planets
		
		self.sphereScaleNode = SceneNode.create(str(id(self)))
		self.orbitLineList = []
		self.orbitLine = LineSet.create()
		self.orbitLine.setEffect('colored -e green')
		#	planetObjList stores the current angle, location and other information of each planet:
		#		name: obj, theta, 
		self.planetObjList = {}
		#self.orbitScaleNode = SceneNode.create(id(self))
	def setVisible(self, visFlag= False):
		self.sphereScaleNode.setChildrenVisible(visFlag)
		self.orbitLine.setVisible(visFlag)
	def setRadiusScale(self):
		list = self.planetObjList
		for planet in list:
			list[planet][1].setScale(Vector3(1,1,1)*self.radiusScale/self.orbitScale)
	def setOrbitScale(self):
		self.orbitLine.setScale(Vector3(1,1,1)*self.orbitScale)
		self.sphereScaleNode.setScale(Vector3(1,1,1)*self.orbitScale)
		self.setRadiusScale()
		for seg in self.orbitLineList:
			seg.setThickness( self.lineThickness / self.orbitScale )
	@staticmethod
	def getData(str, type, default):
		if str == None:
			return default
		else:
			return type(str)
	@staticmethod
	def getElipsePosition(theta, majorAxis, eccentricity, inclination, periastron = 0.0, ascendingNode = 0.0):
		radius = majorAxis * (1 - eccentricity*eccentricity) / (1- eccentricity*cos(radians(theta)))
		x = cos(radians(theta-periastron)) * cos(radians(inclination)) * radius
		y = sin(radians(theta-periastron)) * radius
		z = cos(radians(theta-periastron)) * sin(radians(inclination)) * radius
		r = sqrt( x**2 + y**2 )
		thetaPrime = radians(theta-periastron) + radians(ascendingNode)
		x = r * cos(thetaPrime)
		y = r * sin(thetaPrime)
		return Vector3(x, z, y)
	def setPlanetPosition(self, theta, name):
		target = self.planetObjList[name]
		if theta > 360.0:
			theta -= 360.0
		target[0] = theta
		target[1].setPosition( self.getElipsePosition( theta, target[4], target[6], target[5], target[7], target[8] ) )
	def running(self, dt):
		planetList = self.planetObjList
		for name in planetList:
			self.planetRotate(1000 * dt * self.speedScale /planetList[name][2], name)
			planetList[name][1].yaw(radians(1000 * dt * self.speedScale /planetList[name][3]))
	def planetRotate(self, delta, name):
		target = self.planetObjList[name]
		target[0] += delta
		if target[0] > 360.0:
			target[0] -= 360.0
		target[1].setPosition( self.getElipsePosition( target[0], target[4], target[6], target[5], target[7], target[8]  ) )
	def drawSystem(self, visFlag = False):
		#self.testLine = LineSet.create()
		#self.testLine.setEffect('colored -e green')
		for star in self.starList:
			self.drawStar( star )
		for planet in self.planetList:
			self.drawPlanet( planet )
		self.setVisible(visFlag)
	def drawPlanet(self, planet):
		# Draw orbit
		# Segments # is defined by fineLevel
		#		1 - 36 up to 10 - 360
		majorAxis = self.getData( planet['semimajoraxis'], float, 1.0)
		inclination = self.getData( planet['inclination'], float, 0.0 )
		eccentricity = self.getData( planet['eccentricity'], float, 0.0 )
		periastron = self.getData( planet['periastron'], float, 0.0 )
		ascendingnode = self.getData( planet['ascendingnode'], float, 0.0 )
		radius = self.getData( planet['radius'], float, 0.0 )
		year = self.getData(planet['period'], float, 365.0)
		day = self.getData(planet['day'], float, 1.0)
		tilt = self.getData(planet['axistilt'], float, 0.0)
		#
		#	Draw orbits.
		#
		if self.fineLevel > 0:
			interval = 10.0 / self.fineLevel
			theta = 0.0
			while theta <= 360:
				line = self.orbitLine.addLine()
				line.setStart (self.getElipsePosition(theta, majorAxis, eccentricity, inclination, periastron, ascendingnode) )
				theta += interval
				line.setEnd (self.getElipsePosition(theta, majorAxis, eccentricity, inclination, periastron, ascendingnode) )
				self.orbitLineList.append(line)
		#
		#	Draw planets
		#
		name = planet['name']
		phase = 0
		#obj = SphereShape.create(radius, 4)
		obj = BoxShape.create(radius, radius, radius)
		obj.pitch(radians(tilt))
		self.sphereScaleNode.addChild(obj)
		self.planetObjList.update({ name: [phase, obj, year, day, majorAxis, inclination, eccentricity, periastron, ascendingnode]})
		self.setPlanetPosition( 0, name)
	def drawStar(self, star):
		print "Star"