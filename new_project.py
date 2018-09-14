import configparser as cfg
import argparse
import os
import shutil
import paramiko

from flags import Flags
from xml_builder import buildProject


def createArgParser():
	parser = argparse.ArgumentParser(description='Create new project from project template')
	parser.add_argument('-p', '--project-name', help='Name of the new project')
	parser.add_argument('-t', '--template', help='Project template to use')
	parser.add_argument('-d', '--dest-root', help='Destination root directory')
	parser.add_argument('-f', '--force', action='store_true', help='Overwrite existing project')
	parser.add_argument('-m', '--macro', dest='macros', action='append',
						help='Specify macro and value: NAME=VALUE')
	return parser;


def parseArgs(parser, flags):
	args = parser.parse_args()

	if args.project_name:
		flags.cfgList['PROJECT_NAME'] = args.project_name
	if args.template:
		flags.cfgList['TEMPLATE'] = args.template
	if args.dest_root:
		flags.cfgList['DEST_ROOT'] = args.dest_root

	flags.force = args.force

	if args.macros:
		for macro in args.macros:
			mSplit = macro.split('=')
			if len(mSplit) < 2:
				print('Error parsing macro argument: ' + macro)
				continue
			flags.macroList[mSplit[0]] = mSplit[1]


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


def printConfig(flags):
	print('\nCONFIG:\n')
	for key in flags.cfgList:
		print(key + ' = ' + flags.cfgList[key])

	print('\nMACROS:\n')
	for key in flags.macroList:
		print(key + ' = ' + flags.macroList[key])


def copyTemplate(templateDir, destDir):
	shutil.copytree(templateDir, destDir)
	if os.path.isfile(destDir + '/template.conf'):
		os.remove(destDir + '/template.conf')


def setupRemote(destDir, flags):
	if flags.cfgList['GIT_SERVER_ADDRESS'] == '' or flags.cfgList['GIT_SERVER_USER'] == '':
		return

	# server setup
	sshAddr = flags.cfgList['GIT_SERVER_ADDRESS']
	sshUser = flags.cfgList['GIT_SERVER_USER']
	sshPath = flags.cfgList['GIT_SERVER_PATH']
	projName = flags.cfgList['PROJECT_NAME']

	# command to run on the server
	sshComm = 'cd '+sshPath+'/.pulautin/; ./new_repository.sh '+projName+'; cd ..; ls -a'

	ssh = paramiko.SSHClient()
	ssh.load_system_host_keys()
	ssh.connect(sshAddr, 22, sshUser)
	ssh_stdin, ssh_stdout, ssh_stderr = ssh.exec_command(sshComm)
	
	#print(destDir)

	os.chdir(destDir)
	os.system('ls -a')
	os.system('git init')
	os.system('git add --all')
	os.system('git commit -m "Initial Commit"')
	os.system('git remote add origin '+sshUser+'@'+sshAddr+':'+sshPath+projName)
	os.system('git push -u origin master')


def main():
	# Load initial config
	cfgList = {}
	macroList = {}
	flags = Flags()
	loadConfig('pulautin.conf', flags)

	# Parse command line arguments
	parser = createArgParser()
	parseArgs(parser, flags)

	# Specify template directory, check for existence
	templateDir = 'templates/projects/' + flags.cfgList['TEMPLATE'] + '/'
	if not os.path.isdir(templateDir):
		print('ERROR: project template from directory \'' + templateDir +'\' not found')
		printConfig(flags)
		return 1

	printConfig(flags) # TEMP

	# Check for configuration errors
	if flags.cfgList['PROJECT_NAME'] == '':
		print("Error: Please provide project name (option -p)")
		return 1

	if flags.cfgList['DEST_ROOT'] == '':
		print("Error: Please provide destination root directory (option -d)")
		return 1

	destDir = flags.cfgList['DEST_ROOT'] + '/' + flags.cfgList['PROJECT_NAME'] + '/'
	if os.path.isdir(destDir):
		if flags.force:
			shutil.rmtree(destDir)
		else:
			print('Error: directory \'' + destDir + '\' already exists')
			return 1

	# Copy template to destination directory
	copyTemplate(templateDir, destDir)

	# Build the project according to the XML
	buildProject(destDir, flags)

	setupRemote(destDir, flags)

main()