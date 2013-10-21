from omega import *
from omegaToolkit import *
from fun import *
from xmlReader import *
from orbit import *
from multiples import *
from galaxy import *
from wand import *


allSystem = {}
globalOrbitScale = 5.0
globalRadiusScale = 0.5
getSceneManager().displayWand(0, 1)


def updateFunction(frame, t, dt):
	global systemInCave
	global galaxy
	if systemInCave != None:
		systemInCave.running(dt)
	galaxy.yaw(dt*radians(10))
	
def setGlobalOrbitScale(scale = 5.0):
	global globalOrbitScale
	globalOrbitScale = scale
	multiples.orbitScale.setFloat(scale)
	PlanetarySystem.orbitScale = scale
	if systemInCave != None:
		systemInCave.setOrbitScale()

def setGlobalRadiusScale(scale = 0.2):
	global globalRadiusScale
	globalRadiusScale = scale
	multiples.radiusScale.setFloat(scale)
	PlanetarySystem.radiusScale = scale
	if systemInCave != None:
		systemInCave.setRadiusScale()

def setRotationSpeedScale(scale):
	PlanetarySystem.speedScale = scale

def moveMultiple(x, y, z):
	print x, ' ', y, ' ', z
		
#
#	Here h and v should be in range(1,8)
#
def addMultipleToWall(multiple, h, v):
	global rootNode
	global column
	global row
	global cam
	if column < h or row < v:
		print "out of range"
		return None
	else:
		print "construct"
		multiple.multiple.setPosition(Vector3(-0.5, 0, 0.01) + multiple.multiple.getPosition())
		if h >= 4:
			h+=3
		v -= 1
		hLoc = h + 0.5
		degreeConvert = 36.0/360.0*2*pi #18 degrees per panel times 2 panels per viz = 36
		caveRadius = 3.25
		screenCenter = multiple.parentNode
		screenCenter.setPosition(Vector3(sin(hLoc*degreeConvert)*caveRadius, v * 0.29 + 0.41, cos(hLoc*degreeConvert)*caveRadius))
		screenCenter.yaw(hLoc*degreeConvert+radians(180))
		rootNode.addChild(screenCenter)
		return screenCenter

#
#	Read all files and initialize
#

cam = getDefaultCamera()
rootNode = SceneNode.create("systemOnWall")
cam.addChild(rootNode)
column = 6
row = 8
systemDir = "./stellar/"
multiples.initialize()
systemDic = readAllFilesInDir(systemDir)

multiples.radiusRatio.setFloat(4.0)
multiples.orbitRatio.setFloat(8.0)

skybox = Skybox()
skybox.loadCubeMap('./model/skybox/', 'png')
getSceneManager().setSkyBox(skybox)
cam.setPosition(Vector3( 10, 2, 10 ))
cam.yaw(radians(45))
cam.pitch(radians(-10))

# for h in range(1,9):
	# for v in range(1,9):
		# outlineBox = SphereShape.create(0.125, 4)
		# addMultipleToWall( outlineBox, h, v)
def loadAllSystem():
	h = 1;
	v = 0;
	global galaxy
	global galaxyCore
	global containerToSystemMap
	global targetList
	(galaxy,galaxyCore) = buildGalaxy(systemDic)
	for systemName in systemDic:
		stellar = PlanetarySystem(systemDic[systemName]['star'], systemDic[systemName]['planets'], systemName)
		stellarMultiple = multiples(systemDic[systemName])
		v+=1;
		if v > row:
			v = 1
			h+=1
		addMultipleToWall(stellarMultiple, h, v)
		stellar.drawSystem(False)
		allSystem.update( {systemName: [stellar, stellarMultiple]} )
		stellarMultiple.multiple.setSelectable(True)
		targetList.append(stellarMultiple.multiple)
		containerToSystemMap.update( {stellarMultiple.multiple: [stellar]} )
		if v == row and h == column:
			break;



loadAllSystem()
switchSystemInCave(allSystem['Sun'][0])
attachUpdateFunction(updateFunction)

# galaxy = buildGalaxy(systemDic)
# systemName = "Kepler-33"
# stellar = PlanetarySystem(systemDic[systemName]['star'], systemDic[systemName]['planets'], systemName)
# stellarMultiple = multiples(systemDic[systemName])
# stellarMultiple.parentNode.setPosition(Vector3( -2, 2, -4))
# stellar.drawSystem(False)
# systemName = "Sun"
# stellar2 = PlanetarySystem(systemDic[systemName]['star'], systemDic[systemName]['planets'], systemName)
# stellarMultiple2 = multiples(systemDic[systemName])
# stellarMultiple2.parentNode.setPosition(Vector3( 0.5, 2, -4))
# stellar2.drawSystem(False)
# switchSystemInCave(stellar2)



