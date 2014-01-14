#EU4Parser

A Python utility for converting EU4 save and config files to a JSON-encoded string. It utilizes the PyParsing library to parse the files.

##Requirements

-	Python 3.x
-	PyParsing library

##Usage example

from eu4_parser import *
import os

	filename = 	'c:\\MySaveFolder\\my_save_file.eu4'
	parser = EU4Parser()
	result = parser.parse_file(filename)
	outfile = open(os.getcwd()+"\\result.txt","w")
	outfile.write(result)
	outfile.close()
