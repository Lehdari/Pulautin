import xml.etree.ElementTree as et
import os
import glob


def parseMacros(rootNode, macroList):
	macrosNode = rootNode.find('macros')
	if macrosNode:
		for m in macrosNode.iter('macro'):
			macroList[m.attrib['name'].upper()] = m.attrib['value']


def applyMacros(str, macroList):
	for m, val in macroList.items():
		mm = '{{' + m + '}}'
		str = str.replace(mm, val)

	return str;


def buildFile(fileName, fNode):
	f = open(fileName, "w")

	macroList = {}
	parseMacros(fNode, macroList)

	for fElem in list(fNode):
		if fElem.tag == 'section':
			sMacroList = macroList.copy()
			parseMacros(fElem, sMacroList)

			stripLines = False
			if 'strip' in fElem.attrib and fElem.attrib['strip'] == 'true':
				stripLines = True

			if 'template' in fElem.attrib:
				with open('templates/files/' + fElem.attrib['template']) as ft:
					for line in ft:
						f.write(applyMacros(line, sMacroList))
			else:
				
				for line in fElem.text.splitlines(1):
					if stripLines:
						line = line.lstrip()
					f.write(applyMacros(line, sMacroList))

	f.close()


def buildProject(projectPath, cfgList={}, macroList={}):
	tree = et.parse(projectPath + 'pulautin.xml')
	root = tree.getroot()

	# check for root node
	if not root.tag == 'project':
		print('Error: pulautin.xml is not valid (no root node named project)')
		return

	# parse macros
	parseMacros(root, macroList)

	# create files
	for fNode in root.findall('file'):
		fileName = projectPath + fNode.attrib['name'];
		if os.path.isfile(fileName):
			os.remove(fileName)

		buildFile(fileName, fNode)

	# apply global macros
	for fileName in glob.iglob(projectPath + '**/*', recursive=True):
		if os.path.isdir(fileName):
			continue

		f = open(fileName, "r")
		fRaw = f.read()
		f.close()
		f = open(fileName, "w")
		f.write(applyMacros(fRaw, {**cfgList, **macroList}))
		f.close()