#!/usr/bin/python
# -*- coding: Cp1250 -*-
'''
Created on 04-07-2012

Small utility to convert polish characters from unicode coding to UTF characters.

@author: Mariusz Jakubowski
'''

import sys


conv = {
        "\u0119": "�",            "\u0118": "�",
        "\u00F3": "�",            "\u00D3": "�",
        "\u0105": "�",            "\u0104": "�",
        "\u015B": "�",            "\u015A": "�",
        "\u0142": "�",            "\u0141": "�",
        "\u017C": "�",            "\u017B": "�",
        "\u017A": "�",            "\u0179": "�",
        "\u0107": "�",            "\u0106": "�",
        "\u0144": "�",            "\u0143": "�"        
}


allFile = open(sys.argv[1], "r")
allText = allFile.read()
allFile.close()
for k in conv.keys():
    allText = allText.replace(k, conv[k])
allFile = open(sys.argv[1], "w")
allFile.write(allText)
allFile.close()
