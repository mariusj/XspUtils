#!/usr/bin/python
# -*- coding: Cp1250 -*-
'''
Created on 04-07-2012

Small utility to convert polish characters from unicode coding to UTF characters.

@author: Mariusz Jakubowski
'''

import sys


conv = {
        "\u0119": "ę",            "\u0118": "Ę",
        "\u00F3": "ó",            "\u00D3": "Ó",
        "\u0105": "ą",            "\u0104": "Ą",
        "\u015B": "ś",            "\u015A": "Ś",
        "\u0142": "ł",            "\u0141": "Ł",
        "\u017C": "ż",            "\u017B": "Ż",
        "\u017A": "ź",            "\u0179": "Ź",
        "\u0107": "ć",            "\u0106": "Ć",
        "\u0144": "ń",            "\u0143": "Ń"        
}


allFile = open(sys.argv[1], "r")
allText = allFile.read()
allFile.close()
for k in conv.keys():
    allText = allText.replace(k, conv[k])
allFile = open(sys.argv[1], "w")
allFile.write(allText)
allFile.close()
