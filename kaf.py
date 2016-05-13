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
CHECK_PATH = WORKING_DIR + '/check/'
version = "Version 1.0.5"

# =======================
#     MENUS FUNCTIONS
# =======================

def main_menu():
    os.system('clear')
    
    print colored("""
----        -----         ------          ------------
|    |      /    /        /      \        |            |
|    |     /    /        /        \       |    --------
|    |    /    /        /    /\    \      |    |%%%%%%%
|    |   /    /        /    /%%\    \     |    |
|     --     /---------     ----     ------    --------
|     --     \---------     ----     ------    --------
|    |%%%\    \%%%%% /     /%%%%%\     \  |    |%%%%%%%
|    |    \    \    /     /       \     \ |    |
|    |     \    \  /     /         \     \|    |
|    |      \    \/     /           \     \    |
|    |       \    \    /             \     \   |
----         -----  --               ------ --%
%%%%         %%%%%  %%               %%%%%% %%  
""", 'green')
    print
    print colored("<< WELCOME TO KICK-ASS-FRAMEWORK >> \n       " + version  +"\n", 'red')
    print colored("Please choose :\n", 'white')
    print "1. HELP"
    print "2. KA-SHELL"
    print "3. LIST EXPLOITS"
    print "4. UPDATE EXPLOIT DB"
    print colored("\n0. QUIT", 'white')
    choice = raw_input(colored(" >> ", 'white'))
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
    print colored("HELP \n KAF (KickAssFramework) " + version  + "\n Find us: http://kickassugvgoftuk.onion \n", 'white')  
    print " *commands in KA-SHELL \n"
    print " use <module_name> (use exploit)"
    print " search <module_name> (search exploit)"
    print " list (list exploits)"
    print " exit (quit the shell)\n"
    print colored("Please choose :\n", 'white')
    print colored("2. KA-SHELL" , 'white')
    print colored("9. MENU", 'white')
    choice = raw_input(" >>  ")
    exec_menu(choice)
    return

def shell():
    print colored("KA-SHELL  \n", 'white')
    user_name = colored("root", 'red') + colored("@KICKASS", 'blue') + colored(':~$ ', 'white')
    call(["clear"])
    
    while True:
        command = raw_input(user_name)
        if "help" in command:
            print colored("HELP \n KAF (KickAssFramework) " + version  + "\n Find us: http://kickassugvgoftuk.onion \n", 'white')
            print " use <module_name> (use exploit)"
            print " search <module_name> (search exploit)"
            print " list (list exploits)"
            print " exit (quit the shell)\n"
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
                call([command])
            except:
                print colored("[!] Unknown command :-(", 'red') + colored(" . Type 'help' or 'exit' ", 'yellow')    
    exec_menu("9")
    return

def exploits():
    print colored("LIST EXPLOITS \n", 'white')
    for file in os.listdir(EXPLOIT_PATH):
        print "[+] Module name: ", file
    print colored("\nPlease choose :\n", 'white')
    print colored("2. KA-SHELL" , 'white')
    print colored("9. MENU", 'white')
    choice = raw_input(" >>  ")
    exec_menu(choice)
    return

def update():
    print colored("UPDATE EXPLOIT DB \n", 'white')
    print colored("[+] Checking for updates.", 'yellow')
    print "\n"

    try:
        update = urllib2.urlopen('https://raw.githubusercontent.com/c3nt3rX/kaf/master/update.html').read()
        links = re.split(r"[\[\+\]]", update)
        for link in links:
            if link != "":
                filename = link.split('/exploits/', 1)[-1]
                filename = filename.replace("\n", "")
                if not os.path.exists("exploits\\"+filename):
                      try:
                            file_to_download = urllib.URLopener()
                            file_to_download.retrieve(link, filename)
                            shutil.move(filename, "exploits")
                            print colored("[+] Downloading module: " + filename, 'blue')
                      except:
                            pass

        update = urllib2.urlopen('https://raw.githubusercontent.com/c3nt3rX/kaf/master/update2.html').read()
        links = re.split(r"[\[\+\]]", update)
        for link in links:
            if link != "":
                filename = link.split('/check/', 1)[-1]
                filename = filename.replace("\n", "")
                if not os.path.exists("check\\"+filename):
                      try:
                            file_to_download = urllib.URLopener()
                            file_to_download.retrieve(link, filename)
                            shutil.move(filename, "check")
                            print colored("[+] Downloading module: " + filename, 'blue')
                      except:
                            pass
    except:
        print "An error occured! Please try again later."

   
    print colored("[!] An error occured! Please try again later.", 'yellow')    
    print colored("Please choose :\n", 'white')
    print colored("9. MENU", 'white')
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
    '3': exploits,
    '4': update,
    '9': Menu,
    '0': exit,
}

# =======================
#      MAIN PROGRAM
# =======================

if __name__ == "__main__":
    main_menu()