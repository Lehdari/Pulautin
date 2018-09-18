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


def parseArgs(parser, flags):
	args = parser.parse_args()

	if args.project_path:
		flags.cfgList['PROJECT_PATH'] = args.project_path
		pathSplit = args.project_path.split('/') # parse project name from path
		if pathSplit[-1] == '':
			pathSplit.pop()
		flags.cfgList['PROJECT_NAME'] = pathSplit[-1]

	if args.macros:
		for macro in args.macros:
			mSplit = macro.split('=')
			if len(mSplit) < 2:
				print('Error parsing macro argument: ' + macro)
				continue
			macroList[mSplit[0]] = mSplit[1]


def loadConfig(fileName, flags):
	config = cfg.ConfigParser()
	config.read(fileName)

	for section in config:
		if section == 'MACROS':
			for key in config[section]:
				flags.macroList[key.upper()] = config[section][key]
		else:
			for key in config[section]:
				if key.upper() == 'MACRO_FILE_EXTENSIONS':
					flags.macroFileExtensions = config[section][key].split(' ')
				else:
					flags.cfgList[key.upper()] = config[section][key]


def printConfig(cfgList, flags):
	print('\nCONFIG:\n')
	for key in flags.cfgList:
		print(key + ' = ' + flags.cfgList[key])

	print('\nMACROS:\n')
	for key in flags.macroList:
		print(key + ' = ' + flags.macroList[key])


def main():
	# Load initial config
	flags = Flags()
	loadConfig(flags.dir + 'pulautin.conf', flags)

	# Parse command line arguments
	parser = createArgParser()
	parseArgs(parser, flags)

	# Check for configuration errors
	if flags.cfgList['PROJECT_PATH'] == '':
		print("Error: Please provide project path")
		return 1

	destDir = flags.cfgList['PROJECT_PATH'] + '/'
	if not os.path.isdir(destDir):
		print('Error: directory \'' + destDir + '\' does not exist')
		return 1

	buildProject(destDir, flags)

	printConfig(flags.cfgList, flags)


main()