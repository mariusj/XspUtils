'''
Created on 25-06-2012

@author: Mariusz Jakubowski
'''

import sys
import os


auto_trans_dict = None


def get_files(base, adir):
    '''
        Returns a list of all files from a directory base/adir with .properties extension.
    '''   
    path = os.path.join(base, adir)
    filesList = [x for x in os.listdir(path) if x.endswith(".properties")]
    filesList = map(lambda x : os.path.join(adir, x), filesList)
    return filesList



def get_files_by_lang(filesList):
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
    

def create_lang_file(filesByLang, lang, path):
    '''
        Creates a file with joined all .properties files for a given language 
    '''
    langName = "all_" + lang + ".properties" 
    print("  - " + langName)
    allFile = open(os.path.join(path, langName), "w")
    for f in filesByLang[lang]:
        inFile = open(os.path.join(path, f), "r")
        content = ""
        is_content = False
        for line in inFile:
            if not line.startswith("#"):
                content += auto_translate(line)
                is_content = True
            content += line
        if is_content:
            # ignore empty file
            allFile.write("#! " + f + "\n")
            allFile.write(content)
            allFile.write("\n")
        inFile.close()
    allFile.close()


def auto_translate(line):
    '''
        Translates the line using default dictionary.
    '''
    return line

def init_auto_trans():
    '''
        Intialize auto translate dictionary.
    '''
    global auto_trans_dict
    auto_trans_file = open("auto_trans.txt", "r")
    auto_trans_dict = {}
    clang = ""
    for line in auto_trans_file:
        if line.startswith("\n"):
            continue
        print("@"+line+"@")
        if line.find("=") == -1:
            clang = line.rstrip("\n\r")
            auto_trans_dict[clang] = {}
        else:
            key, value = line.split("=")
            auto_trans_dict[clang][key] = value
    auto_trans_file.close() 


def exp(path):
    '''
        Joins all files with .properties extension by language.  
    '''
    print("collecting files in " + path)
    filesList = get_files(path, "XPages") + get_files(path, "CustomControls")
    print("sorting by language")
    filesByLang = get_files_by_lang(filesList)
    print("initializing auto translate")
    init_auto_trans()
    print("writing language files:")
    for l in filesByLang.keys():
        create_lang_file(filesByLang, l, path)
    

if __name__ == '__main__':
    if (len(sys.argv) > 1):
        exp(sys.argv[1])
    else:
        exp(os.getcwd())
