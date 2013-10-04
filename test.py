from proj_2 import *

dataDir = './data/'

list = readPlanetarySystemFile('starList', dataDir)

readPlanetsFile(list, 'planetsList_tmp.csv', dataDir)
