from omega import *
from cyclops import *
from math import *
from euclid import *



class multiples(object):
	
	stellarColorMap = { 'A': Color('white'), 'F': Color('#6599FF'), 'G': Color('yellow'), 'K': Color('orange'), 'M':Color('red') }
	
	orbitScale = Uniform.create('orbitScale', UniformType.Float, 1)
	radiusScale = Uniform.create('radiusScale', UniformType.Float, 1)
	#glowPower = Uniform.create('unif_Glow', UniformType.Float, 1)
	#starColor = Uniform.create('star_color', UniformType.Color, 1)
	cutOffX = Uniform.create('cutoff_x', UniformType.Float, 1)
	cutOffY = Uniform.create('cutoff_y', UniformType.Float, 1)
	offPanelSize = Uniform.create('off_size', UniformType.Float, 1)

	multipleScale = 0.05
	height = 5.0
	width = 40.0
	offsize = 0.2
	
	radiusRatio = 20.0

	@staticmethod
	def getData(str, type, default):
		if str == None:
			return default
		else:
			return type(str)

	@classmethod
	def initialize(cls):
		multipleScale = cls.multipleScale
		width = cls.width * multipleScale
		height = cls.height * multipleScale
		
		cls.orbitScale.setFloat(1.0)
		cls.radiusScale.setFloat(1.0)
		#cls.glowPower.setFloat(20)
		#cls.starColor.setColor(Color(1, 0, 0, 1))
		cls.cutOffX.setFloat(width - cls.offsize*multipleScale)
		cls.cutOffY.setFloat(height - cls.offsize*multipleScale)
		cls.offPanelSize.setFloat(cls.offsize * cls.multipleScale)
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
		multiple.setEffect("background -t")
		
		self.multiple = multiple
		self.starRadius = system['star'][0]['radius']
		#	This is supposed to be set to the parentNode for it to attach to.
		self.parentNode = SceneNode.create('stellar'+system['stellar']['name'])
		self.radiusUniform = multiple.getMaterial().addUniform('unif_Glow', UniformType.Float)
		self.radiusUniform.setFloat(sqrt(self.starRadius) * self.radiusRatio)
		#multiple.setPosition(Vector3(width/2, 0, -10))
		#multiple.setPosition(Vector3(-self.width/2, -8, -10))
		#
		#	might change it. 
		#		Cause different star has different color
		#		And different size						
		#
		stellar = system['stellar']
		distance = self.getData(stellar['distance'], float, 100.0)
		name = self.getData(stellar['name'], str, 'anonym')
		spectraltype = self.getData(stellar['name'], str, 'G')
		#multiple.getMaterial().attachUniform(self.starColor)
		multiple.getMaterial().addUniform('star_color', UniformType.Color).setColor(self.stellarColorMap[system['star'][0]['spectraltype']])
		#multiple.getMaterial().attachUniform(self.glowPower)
		
		
		planets = system['planets']
		numOfPlanets = len(planets)
		geom = ModelGeometry.create('sun')
		index = 0
		for planet in planets:
			geom.addVertex(Vector3(self.multipleScale * self.getData(planet['semimajoraxis'], float, 1), 0, 0))
			geom.addColor(Color(1, numOfPlanets, index, self.multipleScale * self.getData(planet['radius'], float, 0.1)))
			name = planet['name']
			print name
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
		material.attachUniform(self.offPanelSize)

		multiple.addChild(planetSystem)