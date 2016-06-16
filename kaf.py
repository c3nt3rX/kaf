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
import platform

# Main definition - constants
menu_actions  = {}  

OS = platform.system()

WORKING_DIR = os.path.dirname(os.path.realpath(__file__))
if "Windows" in OS:
   EXPLOIT_PATH = WORKING_DIR + '\exploits\\'
   CHECK_PATH = WORKING_DIR + '\check\\'
else:
   EXPLOIT_PATH = WORKING_DIR + '/exploits/'
   CHECK_PATH = WORKING_DIR + '/check/'

   version = "Version 1.1.1"
   URL = "http://kickassugvgoftuk.onion"
   banner = """
      __ __ ___    ______
     / //_//   |  / ____/    WELCOME TO KICK-ASS-FRAMEWORK
    / ,<  / /| | / /_        %s
   / /| |/ ___ |/ __/    
  /_/ |_/_/  |_/_/           %s
   """ % (version, URL)


# =======================
#     MENUS FUNCTIONS
# =======================

def main_menu():
   if "Windows" in OS:
      os.system('cls')
   else:
      os.system('clear')

   print colored( banner,'red')
   print
   print colored("Please choose :\n", 'white')
   print "1. MAIN HELP"
   print "2. KAF-SHELL"
   print "3. UPDATE EXPLOIT DB"
   print colored("\n0. QUIT", 'white')
   choice = raw_input(colored(" >> ", 'white'))
   exec_menu(choice)
   return

# Execute menu
def exec_menu(choice):
   if "Windows" in OS:
      os.system('cls')
   else:
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
   print colored("\n HELP \n KAF (KickAssFramework) " + version  + "\n Find us: http://kickassugvgoftuk.onion \n", 'white')  
   print " *commands in KA-SHELL \n"
   print " use <module_name> (use exploit)"
   print " search <module_name> (search exploit)"
   print " list (list exploits)"
   print " exit (quit the shell)\n"
   print colored("Please choose :\n", 'white')
   print colored("2. KA-SHELL" , 'white')
   print colored("9. MENU", 'white')
   print colored("0. QUIT", 'white')
   choice = raw_input(" >>  ")
   exec_menu(choice)
   return

def shell():
   print colored("KA-SHELL  \n", 'white')
   user_name = colored("root", 'red') + colored("@KICKASS", 'blue') + colored(':~$ ', 'white')
   if "Windows" in OS:
      os.system('cls')
   else:
      os.system('clear')

   try:
      while True:
         command = raw_input(user_name)
         if "help" in command:
            print colored("\n KA SHELL HELP \n", 'white')
            print " *commands in KA-SHELL \n"
            print " use <module_name> (use exploit)"
            print " search <module_name> (search exploit)"
            print " list (list exploits)"
            print " exit (quit the shell)\n"
         elif "use" in command:
            remove = ['use', 'search', ' ']
            command = command.split()
            command = ' '.join([i for i in command if i not in remove])
            exploit_name, exploit_extension = os.path.splitext(command)
            found = False
            for file in os.listdir(EXPLOIT_PATH):
               if str(command) == str(file):
                  found = True
                  if "Windows" in OS:
                     if exploit_extension == ".py" or exploit_extension == ".pl" or exploit_extension == ".rb":
                        os.system("exploits\\"+command)
                     elif exploit_extension == ".c":
                        os.system("cl " + command)
                        os.system(exploit_name)
                     elif exploit_extension == ".cpp":
                        os.system("gcc -o " + exploit_name + " " + command)
                        os.system(exploit_name)
                  else:
                     if exploit_extension == ".py":
                        os.system("python exploits/"+command)
                     elif exploit_extension == ".pl":
                        os.system("perl exploits/"+command)
                     elif exploit_extension == ".rb":
                        os.system("ruby exploits/"+command)
                     elif exploit_extension == ".c":
                        os.system("gcc -o " + exploit_name + " " + command)
                        os.system("./"+exploit_name)
                     elif exploit_extension == ".cpp":
                        os.system("g++ -o " + exploit_name + " " + command)
                        os.system("./"+exploit_name)
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
               print "[+] Module: " + fname
               found = True
               if os.path.isdir(path):
                  continue
            if found == False:
               print colored("[!] The explois list is empty.", 'yellow')
         elif "exit" in command:
            break
         else:
            try:
               if "Windows" in OS:
                  os.system(command)
               else:
                  call([command])
            except:
               print colored("[!] Unknown command :-(", 'red') + colored(" . Type 'help' or 'exit' ", 'yellow')
   except KeyboardInterrupt:
      print colored("Type exit to quit KAF.", 'yellow')
   exec_menu("9")
   return

def exploits():
   print colored("\n LIST EXPLOITS \n", 'white')
   for file in os.listdir(EXPLOIT_PATH):
      print "[+] Module name: ", file
   print colored("\nPlease choose :\n", 'white')
   print colored("2. KA-SHELL" , 'white')
   print colored("9. MENU", 'white')
   print colored("0. QUIT", 'white')
   choice = raw_input(" >>  ")
   exec_menu(choice)
   return

def update():
   print colored("UPDATE EXPLOIT DB \n", 'white')
   print colored("[+] Checking for updates.", 'yellow')
   found = False
   print "\n"
   try:
      update = urllib2.urlopen('https://raw.githubusercontent.com/c3nt3rX/kaf/master/update_exp.html').read()
      links = re.split(r"[\[\+\]]", update)
      for link in links:
         if link != "":
            filename = link.split('/exploits/', 1)[-1]
            filename = filename.replace("\n", "")
            if not os.path.exists(EXPLOIT_PATH + filename):
               try:
                  file_to_download = urllib.URLopener()
                  file_to_download.retrieve(link, filename)
                  print colored("[+] Downloading module: " + filename, 'white')                        
                  shutil.move(filename, EXPLOIT_PATH + filename)
                  found = True
               except:
                  pass
      update = urllib2.urlopen('https://raw.githubusercontent.com/c3nt3rX/kaf/master/update_check.html').read()
      links = re.split(r"[\[\+\]]", update)
      for link in links:
         if link != "":
            filename = link.split('/check/', 1)[-1]
            filename = filename.replace("\n", "")
            if not os.path.exists(CHECK_PATH + filename):
               try:
                  file_to_download = urllib.URLopener()
                  file_to_download.retrieve(link, filename)
                  print colored("[+] Downloading check: " + filename, 'white')
                  shutil.move(filename, CHECK_PATH + filename)                        
                  found = True
               except:
                  pass

      if found == True:
         print colored("[!] EXPLOIT DB successfully updated.", 'yellow')
      else:
         print colored("[!] There are no new updates. You run the latest exploits.", 'yellow')
   except:
      print colored("[!] An error occured! Please try again later.", 'yellow')
   print colored("Please choose :\n", 'white')
   print colored("3. UPDATE ONCE MORE", 'white')
   print colored("9. MENU", 'white')
   print colored("0. QUIT", 'white')
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
   '2': shell,
   '3': update,
   '9': Menu,
   '0': exit,
}

# =======================
#      MAIN PROGRAM
# =======================

if __name__ == "__main__":
   main_menu()
