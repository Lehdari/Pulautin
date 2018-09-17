import xml.etree.ElementTree as et
import os
import glob

from flags import Flags


def parseMacros(rootNode, macroList, overwrite=True):
	macrosNode = rootNode.find('macros')
	if macrosNode:
		for m in macrosNode.iter('macro'):
			key = m.attrib['name'].upper()
			if key in macroList and not overwrite:
				continue
			macroList[key] = m.attrib['value']


def applyMacros(str, macroList):
	#print(str)
	for m, val in macroList.items():
		mm = '{{' + m + '}}'
		str = str.replace(mm, val)

	return str;


def buildFile(fileName, fNode, flags):
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
				with open(flags.dir + 'templates/files/' + fElem.attrib['template']) as ft:
					for line in ft:
						f.write(applyMacros(line, sMacroList))
			else:
				
				for line in fElem.text.splitlines(1):
					if stripLines:
						line = line.lstrip()
					f.write(applyMacros(line, sMacroList))

	f.close()


def buildProject(projectPath, flags):
	tree = et.parse(projectPath + 'pulautin.xml')
	root = tree.getroot()

	# check for root node
	if not root.tag == 'project':
		print('Error: pulautin.xml is not valid (no root node named project)')
		return

	# parse macros
	parseMacros(root, flags.macroList, overwrite=False)

	# create files
	filesNode = root.find('files')
	if filesNode:
		for fNode in filesNode.findall('file'):
			fileName = projectPath + fNode.attrib['name'];
			if os.path.isfile(fileName):
				os.remove(fileName)

			buildFile(fileName, fNode, flags)

	# apply global macros
	for fileName in glob.iglob(projectPath + '**/*', recursive=True):
		if os.path.isdir(fileName):
			continue

		# check for file extension
		goodExt = False
		for ext in flags.macroFileExtensions:
			if '.' + fileName.split('.')[-1] == ext:
				goodExt = True
				break

		if not goodExt:
			continue

		f = open(fileName, "r")
		fRaw = f.read()
		f.close()
		f = open(fileName, "w")
		f.write(applyMacros(fRaw, {**flags.cfgList, **flags.macroList}))
		f.close()