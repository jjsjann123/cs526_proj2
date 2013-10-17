from omega import *
from omegaToolkit import *
from xmlReader import *
from orbit import *
from multiples import *

systemInCave = None

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

systemDir = "./stellar/"
multiples.initialize()

cam = getDefaultCamera()

q = readAllFilesInDir(systemDir)

m = multiples(q['Sun'])
m.multiple.setPosition(Vector3(-20, 0, -40))
#cam.addChild(m.multiple)
sun = PlanetarySystem(q['Sun']['star'], q['Sun']['planets'])
sun.drawSystem(True)

systemInCave = sun

		
setUpdateFunction(updateFunction)