#!/usr/bin/env python3
#D34D_5H07
#Shell-Finder
import http.client
import sys
import os
import getopt
from optparse import OptionParser
import string
import signal
import ssl
from time import sleep
import random
import subprocess

red = "\033[1;31;40m"
green = "\033[1;32;40m"
cyan = "\033[1;36;40m"


banner = green + """

███████╗██╗███╗   ██╗██████╗       ██╗████████╗
██╔════╝██║████╗  ██║██╔══██╗      ██║╚══██╔══╝
█████╗  ██║██╔██╗ ██║██║  ██║█████╗██║   ██║   
██╔══╝  ██║██║╚██╗██║██║  ██║╚════╝██║   ██║   
██║     ██║██║ ╚████║██████╔╝      ██║   ██║   
╚═╝     ╚═╝╚═╝  ╚═══╝╚═════╝       ╚═╝   ╚═╝   

[MeX]       Coded By DeadShot        [MeX]

 """
os.system("clear")
print(banner)
print(red+ "[?] Read The README.md Before You Start [?] \n")
logFile = ""

def signal_handler(signal, frame):
	print(red + "\n Scanning Was Stopped By User \n")
	os.system("sleep 1")
	print(green + "Thanks For Using This Tool" +  red +" [MeX] \n")
	sys.exit(0)
signal.signal(signal.SIGINT, signal_handler)

def printMSG(printM):
    print(printM)
    if logFile != "":
        fhandle = open(logFile, "a")
        fhandle.write(printM + "\n")
        fhandle.close()

def cmd(command = None):
    returnArr = {}
    returnArr.update({"returnCode": 99})
    try:
        if command == None or command == "":
            return returnArr
        stdout = ""
        stderr = ""
        reCode = subprocess.Popen(command,shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        stData = reCode.communicate()
        returnArr.update({"stdout": stData[0].decode("utf-8")})
        returnArr.update({"stderr": stData[1].decode("utf-8")})
        returnArr.update({"returnCode": reCode.returncode})
        reCode.terminate()
        return returnArr
    except Exception as ErrMs:
        returnArr.update({"error": ErrMs})
        return returnArr

def main():
    print(green)
    global logFile
    parser = OptionParser( usage="%prog -u http://example.com/en/ -l shell.txt", version="%prog 1.0.3")
    parser.add_option("-u", "--url", dest="targetURL", metavar="URL", help="Target URL to scan")
    parser.add_option("-l", "--list", dest="listFile", metavar="FILE", help="List of paths to scan")
    parser.add_option("-r", "--redirect", action="store_true", dest="showRedirect", help="Show redirect codes (3xx)")
    parser.add_option("-e", "--error", action="store_true", dest="showError", help="Show Error codes (5xx)")
    parser.add_option("-s", "--sleep", dest="milliseconds", type="int", metavar="NUMBER", help="Sleep for x milliseconds after each request")
    parser.add_option("-a", "--header", action="append", dest="headers", help="Add Header to the HTTP request (Ex.: -a User-Agent x)", metavar='HEADER VALUE', nargs=2)
    parser.add_option("-b", "--body", dest="requestBody", metavar="Body", help="Request Body (Ex.: name=val&name2=val2)")
    parser.add_option("-x", "--method", dest="requestMethod", metavar="[Method]", help="HTTP Request Method")
    parser.add_option("-i", "--ignore", action="append", dest="ignoreText", metavar="Text", help="Ignore results that contain a specific string")
    parser.add_option("-m", "--min-response-size", dest="dataLength", type="int", metavar="NUMBER", help="The minimum response body size in Byte")
    parser.add_option("-g", "--log", dest="logFile", metavar="FILE", help="Log scan results to a file")
    parser.add_option("-f", "--start-from", dest="startFrom", type="int", metavar="NUMBER", help="Start scanning from URL number x in the provided list")
    parser.add_option("-t", "--timeout", dest="reqTimeout", type="int", metavar="Seconds", help="Set request timeout.")
    parser.add_option("-v", "--verbose", action="store_true", dest="verbose", help="Show error messages")
    parser.add_option("-d", "--define-variable", action="append", dest="variables", help="Define variables to be replaced in URL (Ex.: -d '$varExtension' 'php')", metavar='VARIABLE VALUE', nargs=2)
    parser.add_option("--cmd", dest="excCMD", metavar="Command", help="For Executing Shell Command)")

    startFrom = 0
    reqTimeout = 15

    (options, args) = parser.parse_args()

    if options.requestMethod == None:
        options.requestMethod = "GET"

    if options.requestBody == None:
        options.requestBody = ""

    if options.dataLength == None:
        options.dataLength = 0

    requestHeaders = {}
    if options.headers == None:
        options.headers = []

    for header in options.headers:
        requestHeaders.update({header[0]: header[1]})

    if options.variables == None:
        options.variables = []

    if options.listFile == None or options.targetURL == None:
        parser.print_help()
        sys.exit()

    if options.logFile != None:
        logFile = options.logFile

    if options.startFrom != None:
        startFrom = options.startFrom

    if options.reqTimeout != None:
        if options.reqTimeout > 0:
            reqTimeout = int(options.reqTimeout)

    excCMD = ""
    if options.excCMD != None:
        excCMD = str(options.excCMD)

    if not os.path.isfile(options.listFile):
        printMSG(green+ "Error: File (" + options.listFile + ") doesn't exist.")
        sys.exit()

    if options.targetURL[-1] != "/":
        options.targetURL += "/"

    targetPro = ""

    if options.targetURL[:5].lower() == 'https':
        targetDomain = options.targetURL[8:].split("/",1)[0].lower()
        targetPath = "/" + options.targetURL[8:].split("/",1)[1]
        connection = http.client.HTTPSConnection(targetDomain, timeout=reqTimeout, context=ssl._create_unverified_context())
        targetPro = "https://"
        printMSG(green+ "Target       : " + targetPro+targetDomain + " (over HTTPS)")
        printMSG(green+ "Path         : " + targetPath)
    elif options.targetURL[:5].lower() == 'http:':
        targetDomain = options.targetURL[7:].split("/",1)[0].lower()
        targetPath = "/"+options.targetURL[7:].split("/",1)[1]
        connection = http.client.HTTPConnection(targetDomain, timeout=reqTimeout)
        targetPro = "http://"
        printMSG(green+ "Target       : " + targetDomain)
        printMSG(green+ "Path         : " + targetPath)
    else:
        targetDomain = options.targetURL.split("/",1)[0].lower()
        targetPath = "/"+options.targetURL.split("/",1)[1]
        connection = http.client.HTTPConnection(targetDomain, timeout=reqTimeout)
        targetPro = "http://"
        printMSG(green+"Target       : " + targetDomain)
        printMSG(green+"Path         : " + targetPath)

    printMSG(green+"Method       : " + options.requestMethod)
    printMSG(green+"Header       : " + str(requestHeaders))
    printMSG(green+"Body         : " + options.requestBody)
    printMSG(green+"Timeout      : " + str(reqTimeout))

    if options.showRedirect != None:
        printMSG("Show Redirect:  ON")
    if options.showError != None:
        printMSG("Show Error   :  ON")

    try:
        randomPage = ''.join([random.choice(string.ascii_lowercase + string.digits) for n in range(16)])
        connection.request(options.requestMethod, targetPath+randomPage+".txt", options.requestBody, requestHeaders)
        res = connection.getresponse()
    except Exception as ErrMs:
        if options.verbose != None:
            printMSG("MainError: " + str(ErrMs))
        sys.exit(0)

    if res.status == 200:
        printMSG("NOTE: Looks like the server is returning code 200 for all requests, there might be lots of false positive links.")

    if res.status >= 300 and res.status < 400 and options.showRedirect != None:
        printMSG("NOTE: Looks like the server is returning code " + str(res.status) + " for all requests, there might be lots of false positive links. try to scan without the option -r")

    tpData = res.read()

    with open(options.listFile) as lFile:
        pathList = lFile.readlines()
    totalURLs = len(pathList)
    printMSG (green+ "Scanning ( " + str(totalURLs) + " ) files...")
    countFound = 0
    countAll = 0
    strLine = ""
    for pathLine in pathList:
        try:
            countAll = countAll + 1
            pathLine = pathLine.strip("\n")
            pathLine = pathLine.strip("\r")
            if countAll < startFrom:
                continue
            if pathLine != "":
                for variable in options.variables:
                    pathLine = pathLine.replace(variable[0], variable[1])
                if pathLine[:1] == "/":
                    pathLine = pathLine[1:]
                print (' ' * len(strLine), "\r", end="")
                strLine = "Checking ["+str(countAll)+"/"+str(totalURLs)+"] "+targetPath+pathLine
                print (strLine,"\r", end="")
                if options.milliseconds != None:
                    sleep(options.milliseconds/1000)
                connection.request(options.requestMethod, targetPath+pathLine, options.requestBody, requestHeaders)
                res = connection.getresponse()
                resBody = res.read().decode("utf-8")
                resBodySize = len(resBody)
                isignored = False
                if options.ignoreText != None:
                    for igText in options.ignoreText:
                        if igText in resBody:
                            isignored = True

                fURL = str(targetPro+targetDomain+targetPath+pathLine)
                redirectHead = ""
                exCommand = False
                if res.getheader("location") != None:
                    redirectHead = str(res.getheader("location"))
                if res.status >= 200 and res.status < 300:
                    if isignored == False and resBodySize >= options.dataLength:
                        exCommand = True
                        print (' ' * len(strLine), "\r", end="")
                        printMSG("Code " + str(res.status) + " : " + fURL + " (" + str(resBodySize) + " Byte)")
                        countFound += 1

                if options.showError != None:
                    if res.status >= 500 and res.status < 600:
                        if isignored == False and resBodySize >= options.dataLength:
                            exCommand = True
                            print (' ' * len(strLine), "\r", end="")
                            printMSG("Code " + str(res.status) + " : " + fURL)
                            countFound += 1

                if options.showRedirect != None:
                    if res.status >= 300 and res.status < 400:
                        if isignored == False and resBodySize >= options.dataLength:
                            exCommand = True
                            print (' ' * len(strLine), "\r", end="")
                            printMSG("Code " + str(res.status) + " : " + fURL + " ( " + redirectHead + " )")
                            countFound += 1

                if str(excCMD) != "" and exCommand == True:
                    cmdStr = str(excCMD)
                    cmdStr = cmdStr.replace("{#CODE#}", str(res.status))
                    cmdStr = cmdStr.replace("{#URL#}", fURL)
                    cmdStr = cmdStr.replace("{#SIZE#}", str(resBodySize))
                    cmdStr = cmdStr.replace("{#REDIRECT#}", redirectHead)
                    cmdRes = cmd(str(cmdStr))
                    if options.verbose != None and isinstance(cmdRes, dict) and 'stdout' in cmdRes:
                        printMSG(cmdRes['stdout'])

        except Exception as ErrMs:
            if options.verbose != None:
                print (' ' * len(strLine), "\r", end="")
                printMSG("Error[" + str(countAll) + "]: " + str(ErrMs))
            try:
                connection.close()
                pass
            except Exception as e:
                if options.verbose != None:
                    printMSG("Error2:" + str(e))
                pass
            
        
    connection.close()
    print (' ' * len(strLine), "\r", end="")
    printMSG( "Total Pages found: " + str(countFound) )



if __name__ == "__main__":
    main()
