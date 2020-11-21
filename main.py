import subprocess
import os
import sys

from xml.dom import minidom
from xml.parsers.expat import ExpatError

# CONSTANTS
SRC_FILES = ["c", "cpp", "cc", "cs"]

#Takes a file name as an input and determines if it is a source file or not
def IsSourceFile(filename):
    is_src = False
    if(filename.find(".") >= 0):
        file_extention = m.filename.split(".")[1]
        if file_extention in SRC_FILES:
            is_src = True
    return is_src

def GetSRCML(source):
    result = subprocess.check_output(['srcml', source])
    return result

def GetVariableNamesFromSRCML(xml_string):
    toReturn = []

    xml = minidom.parseString(xml_string)

    unit = xml.documentElement
    declarations = unit.getElementsByTagName("decl_stmt")

    for x in declarations:
        decl = x.childNodes
        for child in decl[0].childNodes:
            if(child.nodeType != child.TEXT_NODE):
                if(child.tagName == 'name'):
                    for y in child.childNodes: # get variable name
                        if(y.nodeValue != None):
                            toReturn.append(y.nodeValue)
    return toReturn

def GetFunctionNamesFromSRCML(xml_string):
    toReturn = []

    xml = minidom.parseString(xml_string)

    unit = xml.documentElement
    functions = unit.getElementsByTagName("function")

    for func in functions:
        for child in func.childNodes:
            if(child.nodeType != child.TEXT_NODE):
                if(child.tagName == 'name'):
                    for y in child.childNodes: # get variable name
                        if(y.nodeValue != None):
                            toReturn.append(y.nodeValue)
    return toReturn

def IsCamelCase(s):
    return s != s.lower() and s != s.upper() and "_" not in s and s[0] != s[0].upper()

def IsSnakeCase(s):
    return s.find('_') > 0 and s[-1] != '_'

def CountLeadingSpaces(s):
    return len(s) - len(s.lstrip(' '))

def CountLeadingTabs(s):
    return len(s) - len(s.lstrip('\t'))

def main():
    # Constants
    REPO_DIR = "./repos/"
    # parsing arguments
    fileName = sys.argv[1]
    repoURLFile = open(fileName, 'r')

    repoURLs = repoURLFile.readlines()
    repoURLs = repoURLs[0:2] # just taking the first 2 for now for testing purposes

    # clone all of the repositories
    try:
        os.mkdir(REPO_DIR)
    except OSError as error:
        print(error)

    for url in repoURLs:
        parsed = url.strip().split("/")
        directoryName = parsed[-2] + "+" + parsed[-1][:-4]
        subprocess.run(["git", "clone", url.strip(), REPO_DIR + directoryName])


if __name__ == "__main__":
    main()
