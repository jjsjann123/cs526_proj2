from omega import *
from math import *
import os

def hash_string(str, max = 10):
	number = 0
	for letter in str:
		number += ord(letter)
	return number%max
	
randomTextureMap = []
randomDir = './model/random/'
for file in os.listdir(randomDir):
	randomTextureMap.append(randomDir+file)
textureMap = ['Earth', 'Mercury', 'Venus', 'Mars', 'Saturn', 'Jupiter', 'Uranus', 'Neptune']
starTextureDir = './model/star/'
starTextureMap = {'A': 'a.jpg', 'F': 'f.png', 'G': 'g.png', 'K': 'k.png', 'M': 'm.png', 'O': 'o.png'}


habitRange = {'A' : (8.5, 12.5),'F' : (1.5,2.2), 'G' : (0.95, 1.4 ), 'K' : (0.38 , 0.56 ), 'M' : (0.08 ,0.12) }
radiusOfEarth = 0.091130294


discoveryMethod = { 'RV': 1, 'transit': 2, 'imaging': 3, 'timing': 4, None: 5 }

stellarColorMap = { 'A': Color('white'), 'F': Color('#6599FF'), 'G': Color('yellow'), 'K': Color('orange'), 'M':Color('red') }
stellarMap = { 'A': (1, 1, 1), 'F': (65.0/255,99.0/255,1), 'G': (1.0, 1.0, 0.0), 'K': (1.0, 0.65, 0.0), 'M': (1.0, 0.0, 0.0) }

fontSize = 60

galaxy = SceneNode.create('galaxy')
