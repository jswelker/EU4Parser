#copyright Josh Welker (jswelker@gmail.com)
#December 2013

from eu4_parser import *
import os

filename = 	'c:\\MySaveFolder\\my_save_file.eu4'
parser = EU4Parser()
result = parser.parse_file(filename)
outfile = open(os.getcwd()+"\\result.txt","w")
outfile.write(result)
outfile.close()
