from omega import *
from omegaToolkit import *
from xmlReader import *
from orbit import *
from multiples import *

systemInCave = None
cam = getDefaultCamera()
rootNode = SceneNode.create("systemOnWall")
cam.addChild(rootNode)
column = 8
row = 8

def updateFunction(frame, t, dt):
	global systemInCave
	if systemInCave != None:
		systemInCave.running(dt)
	
def setGlobalOrbitScale(scale):
	multiples.orbitScale.setFloat(scale)
	PlanetarySystem.orbitScale = scale
	if systemInCave != None:
		systemInCave.setOrbitScale()

def setGlobalRadiusScale(scale):
	multiples.radiusScale.setFloat(scale)
	PlanetarySystem.radiusScale = scale
	if systemInCave != None:
		systemInCave.setRadiusScale()

def setRotationSpeedScale(scale):
	PlanetarySystem.speedScale = scale

def switchSystemInCave(newSystem):
	global systemInCave
	if systemInCave != None:
		systemInCave.setVisible(False)
	elif systemInCave == newSystem:
		systemInCave.setVisible(True)
	else:
		systemInCave = newSystem
		newSystem.setVisible(True)
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
		if h >= 5:
			h+=1
		v -= 1
		hLoc = h + 0.5
		degreeConvert = 36.0/360.0*2*pi #18 degrees per panel times 2 panels per viz = 36
		caveRadius = 3.25
		screenCenter = multiple.parentNode
		screenCenter.setPosition(Vector3(sin(hLoc*degreeConvert)*caveRadius, v * 0.29 + 0.41, cos(hLoc*degreeConvert)*caveRadius))
		screenCenter.yaw(hLoc*degreeConvert)
		screenCenter.addChild(multiple)
		multiple.parentNode = screenCenter
		rootNode.addChild(screenCenter)
		return screenCenter

#
#	Read all files and initialize
#
systemDir = "./stellar/"
multiples.initialize()
systemDic = readAllFilesInDir(systemDir)


# for h in range(1,9):
	# for v in range(1,9):
		# outlineBox = SphereShape.create(0.125, 4)
		# addMultipleToWall( outlineBox, h, v)

h = 1;
v = 0;
for systemName in systemDic:
	stellar = PlanetarySystem(systemDic[systemName]['star'], systemDic[systemName]['planets'])
	stellarMultiple = multiples(systemDic[systemName])
	v+=1;
	if v > row:
		v = 1
		h+=1
	addMultipleToWall(stellarMultiple, h, v)
	stellar.drawSystem(False)

setUpdateFunction(updateFunction)
