import configparser as cfg
import argparse
import os
import shutil
from xml_builder import buildProject



class Flags:
	def __init__(self):
		self.force = False


def createArgParser():
	parser = argparse.ArgumentParser(description='Create new project from project template')
	parser.add_argument('-p', '--project-name', help='Name of the new project')
	parser.add_argument('-t', '--template', help='Project template to use')
	parser.add_argument('-d', '--dest-root', help='Destination root directory')
	parser.add_argument('-f', '--force', action='store_true', help='Overwrite existing project')
	parser.add_argument('-m', '--macro', dest='macros', action='append',
						help='Specify macro and value: NAME=VALUE')
	return parser;


def parseArgs(parser, cfgList, macroList, flags=None):
	args = parser.parse_args()

	if args.project_name:
		cfgList['PROJECT_NAME'] = args.project_name
	if args.template:
		cfgList['TEMPLATE'] = args.template
	if args.dest_root:
		cfgList['DEST_ROOT'] = args.dest_root
	if flags is not None:
		flags.force = args.force

	if args.macros:
		for macro in args.macros:
			mSplit = macro.split('=')
			if len(mSplit) < 2:
				print('Error parsing macro argument: ' + macro)
				continue
			macroList[mSplit[0]] = mSplit[1]


def loadConfig(fileName, cfgList, macroList):
	config = cfg.ConfigParser()
	config.read(fileName)

	for section in config:
		if section == 'MACROS':
			for key in config[section]:
				macroList[key.upper()] = config[section][key]
		else:
			for key in config[section]:
				cfgList[key.upper()] = config[section][key]


def printConfig(cfgList, macroList):
	print('\nCONFIG:\n')
	for key in cfgList:
		print(key + ' = ' + cfgList[key])

	print('\nMACROS:\n')
	for key in macroList:
		print(key + ' = ' + macroList[key])


def copyTemplate(templateDir, destDir):
	shutil.copytree(templateDir, destDir)
	if os.path.isfile(destDir + '/template.conf'):
		os.remove(destDir + '/template.conf')


def main():
	# Load initial config
	cfgList = {}
	macroList = {}
	flags = Flags()
	loadConfig('pulautin.conf', cfgList, macroList)

	# Parse command line arguments
	parser = createArgParser()
	parseArgs(parser, cfgList, macroList, flags=flags)

	# Specify template directory, check for existence
	templateDir = 'templates/projects/' + cfgList['TEMPLATE'] + '/'
	if not os.path.isdir(templateDir):
		print('ERROR: project template from directory \'' + templateDir +'\' not found')
		printConfig(cfgList, macroList)
		return 1

	# Check for configuration errors
	if cfgList['PROJECT_NAME'] == '':
		print("Error: Please provide project name (option -p)")
		return 1

	if cfgList['DEST_ROOT'] == '':
		print("Error: Please provide destination root directory (option -d)")
		return 1

	destDir = cfgList['DEST_ROOT'] + '/' + cfgList['PROJECT_NAME'] + '/'
	if os.path.isdir(destDir):
		if flags.force:
			shutil.rmtree(destDir)
		else:
			print('Error: directory \'' + destDir + '\' already exists')
			return 1

	# Copy template to destination directory
	copyTemplate(templateDir, destDir)

	buildProject(destDir, cfgList, macroList)

	printConfig(cfgList, macroList) # TEMP



main()