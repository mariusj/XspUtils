'''
Created on 25-06-2012

@author: Mariusz Jakubowski
'''

import sys
import os
import re
from optparse import OptionParser


auto_trans_dict = None

re_trans = re.compile("([\w\(\)\[\]\-\/\\\d@:\.#\{\}]+)=\[(\w+)\| (.*) \]")


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
    

def create_lang_file(filesByLang, lang, path, is_auto_translate, is_strip):
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
                is_content = True
                content += auto_transform(line, is_auto_translate, is_strip)
            else:
                content += line
        if is_content:
            # write only if file contains entries, ignore empty file
            allFile.write("#! " + f + "\n")
            allFile.write(content)
            allFile.write("\n")
        inFile.close()
    allFile.close()


def auto_transform(line, is_auto_translate, is_strip):
    '''
        Translates the line using dictionary.
    '''
    
    if not is_auto_translate and not is_strip:
        return line
    
    match = re_trans.match(line)
    if not match:
        return line
    
    key = match.group(1)
    lang = match.group(2)
    to_trans = match.group(3)
    
    if is_auto_translate:
        # translate using 'all' dictionary
        all_dict = auto_trans_dict["all"]
        if to_trans in all_dict:
            return key + "=" + all_dict[to_trans]
        # translate using dictionary for given langauge
        if lang in auto_trans_dict: 
            lang_dict = auto_trans_dict[lang]
            if to_trans in lang_dict:
                return key + "=" + lang_dict[to_trans]
    
    if is_strip:
        return key + "=" + to_trans + "\n"
    
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
        # format of dicionary is key=value
        # where key is string to translate
        # and value is translated string 
        if line.find("=") == -1:
            clang = line.rstrip("\n\r ")
            auto_trans_dict[clang] = {}
        else:
            key, value = line.split("=")
            auto_trans_dict[clang][key] = value
    auto_trans_file.close() 


def exp(path, is_auto_translate, is_strip):
    '''
        Joins all files with .properties extension by language.  
    '''
    print("collecting files in " + path)
    filesList = get_files(path, "XPages") + get_files(path, "CustomControls")
    print("sorting by language")
    filesByLang = get_files_by_lang(filesList)
    if is_auto_translate:
        print("initializing auto translate")
        init_auto_trans()
    print("writing language files:")
    for l in filesByLang.keys():
        create_lang_file(filesByLang, l, path, is_auto_translate, is_strip)
    

if __name__ == '__main__':
    usage = "usage: %prog [options] [dir]\n\nif dir is not specified a current directory is used"
    parser = OptionParser(usage)
    parser.add_option("-a", "--autotranslate",
                      action="store_true", dest="auto_transform", default=False,
                      help="automatically translate entries according to auto_trans.txt")
    parser.add_option("-s", "--strip",
                      action="store_true", dest="strip", default=False,
                      help="strip langage prefix for untranslated entries eg. '[fr | home]' becomes 'home'")
    (options, args) = parser.parse_args()
    
    if (len(args) > 0):
        db_dir = args[0] 
    else:
        db_dir = os.getcwd() 

    exp(db_dir, options.auto_translate, options.strip)
