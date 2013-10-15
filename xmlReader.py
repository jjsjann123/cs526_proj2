from xml.dom import minidom
import os

systemDir = "./systems/systems/"

def getString(tag):
	return tag.firstChild.data.encode('ascii', 'ignore')

def getChildTag(tag, tagNameList):
	childList = tag.childNodes
	list = tagNameList[:]
	ret = {}
	for node in childList:
		if node.tagName in list:
			tagName = node.tagName.encode('ascii', 'ignore')
			ret.update( {tagName:getString(node) } )
			list.remove(tagName)
	for tagNotFound in list:
		ret.update( {tagNotFound: None} )
	return ret

def readAllFilesInDir(targetDir):
	res = {}
	for file in os.listdir(targetDir):
		system = readFile(targetDir + file)
		res.update( { system["stellar"]["name"] : system } )
	return res

def readFile(file):
# file = systemDir+'HD 10180.xml'
#file = systemDir+'Sun.xml'
#if True:
	fileHandle = open(file)
	fileStr = ""
	for line in fileHandle:
		fileStr += line.strip('\n\t')

	xml = minidom.parseString(fileStr)
	
	planetInfoList = None
	starInfo = None
	stellarInfo = None
	#	get stellar info
	tagNameList = [ "name", "rightascension", "declination", "distance" ]
	tag = xml.getElementsByTagName("system")
	if len(tag) > 0:
		tag = tag[0]
		stellarInfo = getChildTag( tag, tagNameList )
	
		#	get star info
		tagNameList = [ "name", "mass", "radius", "spectraltype", "temperature" ]
		star = tag.getElementsByTagName("star")
		if len(star) > 0:
			star = star[0]
			starInfo = getChildTag( star, tagNameList )

			#	get planets list info
			tagNameList = [ "name", "mass", "radius", "period", "semimajoraxis", "eccentricity", "inclination", "periastron", "ascendingnode", "discoverymethod" ]
			planetsList = star.getElementsByTagName("planet")
			if len(planetsList) > 0:
				planetInfoList = []
				for planet in planetsList:
					planetInfo = getChildTag( planet, tagNameList )
					planetInfoList.append(planetInfo)
			
	return { "stellar": stellarInfo, "star": starInfo, "planets": planetInfoList }

#q = readAllFilesInDir(systemDir)