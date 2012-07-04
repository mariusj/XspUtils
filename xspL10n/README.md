export.py [path]
Joins all *.properties files into one big file.
path - optional path to Lotus Notes project (exported database using Team Development menu). If not given the current directory is used.

This script joins all language files in XPages and CustomControls subdirectories.
The files are first gruped by language (language is taken from filename eg. _en, _pl, _de).
Then a file for each language is written with name all_{la}.properties where {lang} is language code.
For example: two files
XPages/home_en.properties
CustomControls/layout_en.properties
are joined into all_en.properties

This file can be send to translators. When they finish translating the file it can be imported (splitted) into Lotus project.

import.py filetoimport [path]
Splits a translated file into *.properties files in XPages and CustomControls directories.
filetoimport - name of a file to import (eg. all_de.properties)
path - optional path to Lotus Notes project (exported database using Team Development menu). If not given the current directory is used.

This script reads the filetoimport file and writes *.properties files into XPages and CustomControls directories. You can now use Team Development/Sync with On-Disk project in Designer to import these files to Lotus database.
