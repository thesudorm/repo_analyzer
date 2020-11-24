import subprocess
import os
import sys

from xml.dom import minidom
from xml.parsers.expat import ExpatError

# CONSTANTS
SRC_FILES = ["c", "cpp", "cc", "cs", "java"]

#Takes a file name as an input and determines if it is a source file or not
def IsSourceFile(filename):
    is_src = False
    parsed = filename.split(".")
    if(parsed[-1] in SRC_FILES):
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
    DATA_DIR = "./data/"

    # parsing arguments
    fileName = sys.argv[1]
    repoURLFile = open(fileName, 'r')

    repoURLs = repoURLFile.readlines()
    repoURLs = repoURLs[0:2] # just taking the first 2 for now for testing purposes
    repoDirs = []
    dataDirs = []

    try:
        os.mkdir(REPO_DIR)
    except OSError as error:
        print(error)

    try:
        os.mkdir(DATA_DIR)
    except OSError as error:
        print(error)

    # clone all of the repositories
    for url in repoURLs:
        parsed = url.strip().split("/")
        directoryName = parsed[-2] + "+" + parsed[-1][:-4]

        subprocess.run(["git", "clone", url.strip(), REPO_DIR + directoryName])

        repoDirs.append(REPO_DIR + directoryName)
        dataDirs.append(DATA_DIR + directoryName)
        try:
            os.mkdir(DATA_DIR + directoryName)
        except OSError as error:
            print(error)
    
    # convert all source files into XML

    i = 0 # data directory iterator
    x = 1 # file count 

    for folder in repoDirs:
        files = [os.path.join(r,file) for r,d,f in os.walk(folder) for file in f]
        for f in files:
            if IsSourceFile(f):
                # create xml
                subprocess.run(["srcml", f, "-o", dataDirs[i] + "/" + str(x) + ".xml"])
                x = x + 1
        x = 1
        i = i + 1

    # analyze the XML
    print("gitcloneurl,numvars,numcamelcasevars,numsnakecasevars,numfuncs,numcamelcasefuncs,numsnakecasefuncs")
    i = 0
    for folder in dataDirs:

        numberFuncs = 0
        numberCamelCaseFuncs = 0
        numberSnakeCaseFuncs = 0

        numberVars = 0
        numberCamelCaseVars = 0
        numberSnakeCaseVars = 0

        numberTabsIndented = 0
        numberSpacesIndented = 0
        
        files = [os.path.join(r,file) for r,d,f in os.walk(folder) for file in f]
        for f in files:
            xmlFile = open(f, 'r')
            xml = xmlFile.read()

            variables = GetVariableNamesFromSRCML(xml)
            functions = GetFunctionNamesFromSRCML(xml)

            numberVars = len(variables) + numberVars
            numberFuncs = len(variables) + numberFuncs

            for v in variables:
                if IsCamelCase(v):
                    numberCamelCaseVars = numberCamelCaseVars + 1
                if IsSnakeCase(v):
                    numberSnakeCaseVars = numberSnakeCaseVars + 1

            for f in functions:
                if IsCamelCase(f):
                    numberCamelCaseFuncs = numberCamelCaseFuncs + 1
                if IsSnakeCase(f):
                    numberSnakeCaseFuncs = numberSnakeCaseFuncs + 1

        print(repoURLs[i].strip() + "," + str(numberVars) + "," + str(numberCamelCaseVars) + "," + str(numberSnakeCaseVars) + "," + str(numberFuncs) +  "," + str(numberCamelCaseFuncs) + "," + str(numberSnakeCaseFuncs))
        i = i + 1

if __name__ == "__main__":
    main()
