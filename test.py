from proj_2 import *

dataDir = './data/'

#	read file and creates the planetary database:
list = readPlanetarySystemFile('starList', dataDir)
readPlanetsFile(list, 'planetsList_tmp.csv', dataDir)

drawPlanetarySystems(list)
#	draw planetary sytem:

