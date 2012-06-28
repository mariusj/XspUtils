'''
Created on 25-06-2012

@author: Mariusz Jakubowski
'''

import sys
import os


def imp(pathAll, dbdir):
    '''
        Splits a file into several .properties files.  
    '''
    allFile = open(pathAll, "r")
    output = None
    for line in allFile:
        if line.startswith("#!"):
            if output:
                output.close()
            fname = os.path.join(dbdir, line[3:-1])
            print("creating " + fname)
            output = open(fname, "w")
        else:
            if output:
                if line != "\n":
                    output.write(line)
    allFile.close()
    


if __name__ == '__main__':
    if (len(sys.argv) < 2):
        print("import.py filetoimport [dbdir]")
    else:
        dbdir = os.getcwd()
        if len(sys.argv) == 3:
            dbdir = sys.argv[2]
        imp(sys.argv[1], dbdir)

