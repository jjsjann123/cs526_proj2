from proj_2 import *

dataDir = './data/'
caveSystem = None

#	read file and creates the planetary database:
list = readPlanetarySystemFile('starList', dataDir)
readPlanetsFile(list, 'planetsList_tmp_earth.csv', dataDir)

drawPlanetarySystems(list)
#	draw planetary sytem:

cam = getDefaultCamera()
cam.setPosition( Vector3( 0, 0, 5))
sphere = SphereShape.create( 0.1, 4 )

caveSystem = list['Sun']

def onUpdate(frame, t, dt):
	global caveSystem
	planetList = caveSystem.planetObjList
	if caveSystem != None:
		for name in planetList:
			caveSystem.planetRotate(dt * caveSystem.speedScale /planetList[name][2], name)
			planetList[name][1].yaw(dt * caveSystem.speedScale /planetList[name][3])

setUpdateFunction(onUpdate)