import configparser as cfg
import argparse
import os
import shutil

from flags import Flags
from xml_builder import buildProject


def createArgParser():
	parser = argparse.ArgumentParser(description='Create new project from project template')
	parser.add_argument('project_path', help='Path to the project')
	parser.add_argument('-m', '--macro', dest='macros', action='append',
						help='Specify macro and value: NAME=VALUE')
	return parser;


def parseArgs(parser, cfgList, macroList):
	args = parser.parse_args()

	if args.project_path:
		cfgList['PROJECT_PATH'] = args.project_path
		pathSplit = args.project_path.split('/') # parse project name from path
		if pathSplit[-1] == '':
			pathSplit.pop()
		cfgList['PROJECT_NAME'] = pathSplit[-1]

	if args.macros:
		for macro in args.macros:
			mSplit = macro.split('=')
			if len(mSplit) < 2:
				print('Error parsing macro argument: ' + macro)
				continue
			macroList[mSplit[0]] = mSplit[1]


def loadConfig(fileName, cfgList, macroList, flags=None):
	config = cfg.ConfigParser()
	config.read(fileName)

	for section in config:
		if section == 'MACROS':
			for key in config[section]:
				macroList[key.upper()] = config[section][key]
		else:
			for key in config[section]:
				if key.upper() == 'MACRO_FILE_EXTENSIONS':
					if flags is not None:
						flags.macroFileExtensions = config[section][key].split(' ')
				else:
					cfgList[key.upper()] = config[section][key]


def printConfig(cfgList, macroList):
	print('\nCONFIG:\n')
	for key in cfgList:
		print(key + ' = ' + cfgList[key])

	print('\nMACROS:\n')
	for key in macroList:
		print(key + ' = ' + macroList[key])


def main():
	# Load initial config
	cfgList = {}
	macroList = {}
	flags = Flags()
	loadConfig('pulautin.conf', cfgList, macroList, flags=flags)

	# Parse command line arguments
	parser = createArgParser()
	parseArgs(parser, cfgList, macroList)

	# Check for configuration errors
	if cfgList['PROJECT_PATH'] == '':
		print("Error: Please provide project path")
		return 1

	destDir = cfgList['PROJECT_PATH'] + '/'
	if not os.path.isdir(destDir):
		print('Error: directory \'' + destDir + '\' does not exist')
		return 1

	buildProject(destDir, flags, cfgList, macroList)

	printConfig(cfgList, macroList)


main()