from proj_2 import *

dataDir = './data/'

#	read file and creates the planetary database:
list = readPlanetarySystemFile('starList', dataDir)
readPlanetsFile(list, 'planetsList_tmp_earth.csv', dataDir)

drawPlanetarySystems(list)
#	draw planetary sytem:

cam = getDefaultCamera()

cam.setPosition( Vector3( 0, 0, 5))

sphere = SphereShape.create( 0.2, 4 )
