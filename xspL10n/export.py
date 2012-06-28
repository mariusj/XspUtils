'''
Created on 25-06-2012

@author: Mariusz Jakubowski
'''

import sys
import os


def getFiles(base, adir):
    '''
        Returns a list of all files from a directory base/adir with .properties extension.
    '''   
    path = os.path.join(base, adir)
    filesList = [x for x in os.listdir(path) if x.endswith(".properties")]
    filesList = map(lambda x : os.path.join(adir, x), filesList)
    return filesList



def getFilesByLang(filesList):
    '''
        Returns a dictionary of files categorized by language.
        A key in this dictionary is a language symbol (en, de, pl).
        A value in this dictionary is a list of file names.
    '''
    filesByLang = {} 
    for cf in filesList:
        uidx = cf.rfind("_") + 1
        if uidx > 0:
            dotidx = cf.rfind(".")
            if (dotidx - uidx == 2):
                lang = cf[uidx:dotidx]
                if not lang in filesByLang:
                    filesByLang[lang] = []
                filesByLang[lang].append(cf)
                
    # remove unnecessery entries
    for l in filesByLang.keys():
        if len(filesByLang[l]) == 1:
            del filesByLang[l]
    return filesByLang
    

def createLangFile(filesByLang, lang, path):
    '''
        Creates a file with joined all .properties files for a given language 
    '''
    langName = "all_" + lang + ".properties" 
    print("  - " + langName)
    allFile = open(os.path.join(path, langName), "w")
    for f in filesByLang[lang]:
        allFile.write("#! " + f + "\n")
        inFile = open(os.path.join(path, f), "r")
        allFile.write(inFile.read())
        inFile.close()
        allFile.write("\n")
    allFile.close()



def exp(path):
    '''
        Joins all files with .properties extension by language.  
    '''
    print("collecting files")
    filesList = getFiles(path, "XPages") + getFiles(path, "CustomControls")
    print("sorting by language")
    filesByLang = getFilesByLang(filesList)
    print("writing language files:")
    for l in filesByLang.keys():
        createLangFile(filesByLang, l, path)
    

if __name__ == '__main__':
    if (len(sys.argv) > 1):
        exp(sys.argv[1])
    else:
        exp(os.getcwd())
