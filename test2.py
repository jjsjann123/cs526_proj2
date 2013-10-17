from omega import *
from omegaToolkit import *
from xmlReader import *
from orbit import *
from multiples import *

systemDir = "./systems/systems/"
q = readAllFilesInDir(systemDir)

sun = PlanetarySystem(q['Sun']['star'], q['Sun']['planets'])
sun.drawSystem()

systemInCave = sun

def updateFunction(frame, t, dt):
	global systemInCave
	if systemInCave != None:
		systemInCave.running(dt)
		
setUpdateFunction(updateFunction)