from omegaToolkit import *
#from cyclops import *

cam = getDefaultCamera()
cam.setPosition( Vector3( 0, 0, 45))
sphere = SphereShape.create( 0.1, 4 )

orbitScale = Uniform.create('orbitScale', UniformType.Float, 1)
radiusScale = Uniform.create('radiusScale', UniformType.Float, 1)
glowPower = Uniform.create('unif_Glow', UniformType.Float, 1)
starColor = Uniform.create('star_color', UniformType.Color, 1)
cutOffX = Uniform.create('cutoff_x', UniformType.Float, 1)
cutOffY = Uniform.create('cutoff_y', UniformType.Float, 1)

multipleScale = 1.0
height = 8.0
width = 40.0

orbitScale.setFloat(2.0)
radiusScale.setFloat(1.0)
glowPower.setFloat(20)
starColor.setColor(Color(1, 0, 0, 1))
cutOffX.setFloat(width-0.2)
cutOffY.setFloat(height-0.4)

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

multiple = StaticObject.create('stellar')
#multiple.setPosition(Vector3(width/2, 0, -10))
multiple.setPosition(Vector3(-width/2, -8, -10))
multiple.setEffect("background -t")
multiple.getMaterial().attachUniform(glowPower)
multiple.getMaterial().attachUniform(starColor)

axis = [0.38, 0.72, 1, 5.2, 9.5, 30, 39.48]
radius = [ 0.035, 0.086, 0.09, 1, 0.83, 0.35, 0.216]
name = ['Mercury', 'Venus', 'Earth', 'Jupiter', 'Saturn', 'Neptune', 'Pluto']

geom = ModelGeometry.create('sun')
for i in range(0, len(axis)):
	geom.addVertex(Vector3(axis[i], 0, 0.001))
	geom.addColor(Color(1, len(axis), i, radius[i]))
geom.addPrimitive(PrimitiveType.Points, 0, len(axis))
getSceneManager().addModel(geom)

planetSystem = StaticObject.create('sun')
planetSystem.setEffect("planet -t")
material = planetSystem.getMaterial()
material.attachUniform(orbitScale)
material.attachUniform(radiusScale)
material.attachUniform(cutOffX)
material.attachUniform(cutOffY)

multiple.addChild(planetSystem)

multiple2 = StaticObject.create('stellar')
#multiple2.setPosition(Vector3(width/2, 0, -10))
multiple2.setPosition(Vector3(-width/2, 8, -10))
multiple2.setEffect("background -t")
multiple2.getMaterial().attachUniform(glowPower)
multiple2.getMaterial().attachUniform(starColor)

