from xml.dom import minidom
import os

systemDir = "./systems/systems"
os.chdir(systemDir)

def getString(tag):
	return tag.firstChild.data.encode('ascii', 'ignore')

def getChildTag(tag, tagNameList):
	childList = tag.childNodes
	for node in childList:
		if node.tagName == tagName:
			tagName

for file in os.listdir("."):
	fileHandle = open(systemDir + file)
	fileStr = ""
	for line in fileHandle:
		fileStr += line.strip('\n\t')

	xml = minidom.parseString(fileStr)
	#	get stellar position
	tag = xml.getElementsByTagName("name")
	if len(tag) >= 0:
		stellarName = getString(tag[0])
	else:
		stellarName = None
	tag = xml.getElementsByTagName("rightascension")
	if len(tag) >= 0:
		rightAscensionName = getString(tag[0])
	else:
		rightAscensionName = None
	tag = xml.getElementsByTagName("declination")
	if len(tag) >= 0:
		declination = getString(tag[0])
	else:
		declination = None
	tag = xml.getElementsByTagName("distance")
	if len(tag) >= 0:
		distance = getString(tag[0])
	else:
		distance = None
	
	# get star position
	starTag = xml.getElementsByTagName("star")
	
