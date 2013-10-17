from omega import *
from cyclops import *
from math import *
from euclid import *

class multiples(object):

	orbitScale = Uniform.create('orbitScale', UniformType.Float, 1)
	radiusScale = Uniform.create('radiusScale', UniformType.Float, 1)
	glowPower = Uniform.create('unif_Glow', UniformType.Float, 1)
	starColor = Uniform.create('star_color', UniformType.Color, 1)
	cutOffX = Uniform.create('cutoff_x', UniformType.Float, 1)
	cutOffY = Uniform.create('cutoff_y', UniformType.Float, 1)

	multipleScale = 1.0
	height = 8.0
	width = 40.0

	@staticmethod
	def getData(str, type, default):
		if str == None:
			return default
		else:
			return type(str)

	@classmethod
	def initialize(cls):
		width = cls.width
		height = cls.height
		cls.orbitScale.setFloat(2.0)
		cls.radiusScale.setFloat(1.0)
		cls.glowPower.setFloat(20)
		cls.starColor.setColor(Color(1, 0, 0, 1))
		cls.cutOffX.setFloat(width-0.2)
		cls.cutOffY.setFloat(height-0.4)
		geom = ModelGeometry.create('stellar')
		v1 = geom.addVertex(Vector3(0, height/2, 0))
		geom.addColor(Color(0,1,0,0))
		v2 = geom.addVertex(Vector3(0, -height/2, 0))
		geom.addColor(Color(0,0,0,0))
		v3 = geom.addVertex(Vector3(width, height/2, 0))
		geom.addColor(Color(1,1,0,0))
		v4 = geom.addVertex(Vector3(width, -height/2, 0))
		geom.addColor(Color(1,0,0,0))
		geom.addPrimitive(PrimitiveType.TriangleStrip, 0, 4)
		getSceneManager().addModel(geom)

		shaderPath = "./shaders/"
		multipleDraw = ProgramAsset()
		multipleDraw.name = "background"
		multipleDraw.vertexShaderName = shaderPath + "background.vert"
		multipleDraw.fragmentShaderName = shaderPath + "background.frag"
		#multipleDraw.geometryShaderName = shaderPath + "/planet.geom"
		#multipleDraw.geometryOutVertices = 1
		#multipleDraw.geometryInput = PrimitiveType.Points
		#multipleDraw.geometryOutput = PrimitiveType.TriangleStrip
		getSceneManager().addProgram(multipleDraw)

		starDraw = ProgramAsset()
		starDraw.name = "planet"
		starDraw.vertexShaderName = shaderPath + "planet.vert"
		starDraw.fragmentShaderName = shaderPath + "planet.frag"
		starDraw.geometryShaderName = shaderPath + "/planet.geom"
		starDraw.geometryOutVertices = 4
		starDraw.geometryInput = PrimitiveType.Points
		starDraw.geometryOutput = PrimitiveType.TriangleStrip
		getSceneManager().addProgram(starDraw)

	def __init__(self, system):
		multiple = StaticObject.create('stellar')
		self.multiple = multiple
		#multiple.setPosition(Vector3(width/2, 0, -10))
		#multiple.setPosition(Vector3(-self.width/2, -8, -10))
		multiple.setEffect("background -t")
		#
		#	might change it. 
		#		Cause different star has different color
		#		And different size						
		#
		stellar = system['stellar']
		distance = self.getData(stellar['distance'], float, 100.0)
		name = self.getData(stellar['name'], str, 'anonym')
		spectraltype = self.getData(stellar['name'], str, 'G')
		multiple.getMaterial().attachUniform(self.starColor)
		multiple.getMaterial().attachUniform(self.glowPower)
		
		planets = system['planets']
		numOfPlanets = len(planets)
		axis = [0.38, 0.72, 1, 5.2, 9.5, 30, 39.48]
		radius = [ 0.035, 0.086, 0.09, 1, 0.83, 0.35, 0.216]
		name = ['Mercury', 'Venus', 'Earth', 'Jupiter', 'Saturn', 'Neptune', 'Pluto']
		geom = ModelGeometry.create('sun')
		index = 0
		for planet in planets:
			geom.addVertex(Vector3(self.getData(planet['semimajoraxis'], float, 1), 0, 0.01))
			geom.addColor(Color(1, numOfPlanets, index, self.getData(planet['radius'], float, 0.1)))
			index += 1
		geom.addPrimitive(PrimitiveType.Points, 0, numOfPlanets)
		getSceneManager().addModel(geom)
		
		planetSystem = StaticObject.create('sun')
		planetSystem.setEffect("planet -t")
		material = planetSystem.getMaterial()
		material.attachUniform(self.orbitScale)
		material.attachUniform(self.radiusScale)
		material.attachUniform(self.cutOffX)
		material.attachUniform(self.cutOffY)

		multiple.addChild(planetSystem)

