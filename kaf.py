import os
from subprocess import call
from termcolor import colored
import urllib2
import urllib
import re
import shutil

WORKING_DIR = os.path.dirname(os.path.realpath(__file__))
EXPLOIT_PATH = WORKING_DIR + '/exploits/'

username = raw_input("Username to use: ")
user_name = colored(username+"@KICKASS", 'red') + colored(':~$ ', 'white')
call(["clear"])

while True:
	command = raw_input(user_name)
	if "use" in command:
		remove = ['use', 'search', ' ']
		command = command.split()
		command = ' '.join([i for i in command if i not in remove])
		if ".py" in command:
			command = command
		else:
			command = command + ".py"
		found = False
		for file in os.listdir(EXPLOIT_PATH):
    			if str(command) == str(file):
				found = True
				os.system("python exploits/"+command)
		
		if found == False:
			print colored("[!] Cannot find " + command + ". Try search <module_name> ." , 'yellow')
	elif "search" in command:
		remove = ['use', 'search', ' ']
		command = command.split()
		command = ' '.join([i for i in command if i not in remove])
		found = False
		for file in os.listdir(EXPLOIT_PATH):
	    		if command in file:
				print "[+] Module name: ", file
				found = True
		if found == False:
			print colored("[!] No exploits with "+command+" found.", 'yellow')
	elif "list" in command:
		basepath = WORKING_DIR+'/exploits'
		found = False
		for fname in os.listdir(basepath):
	    		path = os.path.join(basepath, fname)
			print fname
			found = True
	    		if os.path.isdir(path):
				continue
		if found == False:
			print colored("[!] The explois list is empty.", 'yellow')
	elif "update" in command:
                try:
                        print colored("[+] Checking for updates.", 'yellow')
                        update = urllib2.urlopen('https://raw.githubusercontent.com/c3nt3rX/kaf/master/update.html').read()
                        links = re.split(r"[\[\+\]]", update)
                        for link in links:
                                if link != "":
                                        filename = link.split('/exploits/', 1)[-1]
                                        filename = filename.replace("\n", "")
                                        print colored("[+] Downloading: " + filename, 'green')
                                        file_to_download = urllib.URLopener()
                                        file_to_download.retrieve(link, filename)
                                        shutil.move(filename, "exploits")
                except:
                        print colored("[!] An error occured! Please try again later.", 'yellow')
	elif "exit" in command:
		break
	else:
		try:
			call([command])
		except:
			print colored("[!] Unknown command :-( . Type 'exit' for exiting.", 'yellow')
