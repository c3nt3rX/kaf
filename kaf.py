#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Import the modules
import sys, os
from subprocess import call
from termcolor import colored
import urllib2
import urllib
import re
import shutil

# Main definition - constants
menu_actions  = {}  

WORKING_DIR = os.path.dirname(os.path.realpath(__file__))
EXPLOIT_PATH = WORKING_DIR + '/exploits/'

# =======================
#     MENUS FUNCTIONS
# =======================

def main_menu():
   os.system('clear')
   
   print
   print "<< WELCOME TO KICK-ASS-FRAMEWORK >> \n"
   print "Please choose :\n"
   print "1. USE HELP"
   print "2. SEARCH"
   print "3. KA-SHELL"
   print "4. LIST EXPLOITS"
   print "5. UPDATE"
   print "\n0. QUIT"
   choice = raw_input(" >>  ")
   exec_menu(choice)

   return

# Execute menu
def exec_menu(choice):
   os.system('clear')
   ch = choice.lower()
   if ch == '':
       menu_actions['main_menu']()
   else:
       try:
           menu_actions[ch]()
       except KeyError:
           print "Invalid selection, please try again.\n"
           menu_actions['main_menu']()
   return

def help():
   print "USE HELP \n"
   print "\n9. Menu"
   choice = raw_input(" >>  ")
   exec_menu(choice)
   return
 
def search():
   print "SEARCH \n"
   print "\n9. Menu"
   choice = raw_input(" >>  ")
   exec_menu(choice)
   return

def shell():
   print "KA-SHELL \n"
   user_name = colored("root", 'red') + colored("@KICKASS", 'blue') + colored(':~$ ', 'white')
   call(["clear"])
   
   while True:
       command = raw_input(user_name)
       if "help" in command:
           print "KA-Shell help\n"
           print "use (use exploit)"
           print "search <module_name> (search exploit)"
           print "list (list exploits)"
           print "update (update exploit list)"
           print "exit (quit the shell)\n"
       elif "use" in command:
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
   print "\n9. Menu"
   choice = raw_input(" >>  ")
   exec_menu(choice)
   return

def exploits():
   print "LIST EXPLOITS \n"
   for file in os.listdir(EXPLOIT_PATH):
       print "[+] Module name: ", file
   print "\n9. Menu"
   choice = raw_input(" >>  ")
   exec_menu(choice)
   return

def update():
   print "UPDATE EXPLOITS \n"
   print "\n9. Menu"
   choice = raw_input(" >>  ")
   exec_menu(choice)
   return

# Menu to main menu
def Menu():
   menu_actions['main_menu']()

# Exit program
def exit():
   sys.exit()

# =======================
#    MENUS DEFINITIONS
# =======================

menu_actions = {
   'main_menu': main_menu,
   '1': help,
   '2': search,
   '3': shell,
   '4': exploits,
   '5': update,
   '9': Menu,
   '0': exit,
}

# =======================
#      MAIN PROGRAM
# =======================

if __name__ == "__main__":
   main_menu()
