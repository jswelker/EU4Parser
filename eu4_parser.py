#Copyright Josh Welker (jswelker@gmail.com)
#December 2014


#import libraries
from pyparsing import *
import json


class EU4Parser(object):

	def __init__(self):
		pass

	def parse_file(self,fileName):
		
		#get the input text file
		file = open(fileName, "r")
		inputText = file.read()

		#remove the first line "EU4txt"
		inputText = inputText.replace("EU4txt","", 1)

		#define data types that might be in the values
		real = Regex(r"[+-]?\d+\.\d*").setParseAction(lambda x: float(x[0]))
		integer = Regex(r"[+-]?\d+").setParseAction(lambda x: int(x[0]))
		yes = CaselessKeyword("yes").setParseAction(replaceWith(True))
		no = CaselessKeyword("no").setParseAction(replaceWith(False))
		quotedString.setParseAction(removeQuotes)
		unquotedString =  "\""+Word(alphanums+"_-?\"")+restOfLine | Word(alphanums+"_-?\"")
		comment = Suppress("#") + Suppress(restOfLine)
		EQ,LBRACE,RBRACE = map(Suppress, "={}")
		
		data = (real | integer | yes | no | quotedString | unquotedString)
		
		#define structures
		value = Forward()
		object = Forward() 
		
		dataList = Group(OneOrMore(data))
		simpleArray = (LBRACE + dataList + RBRACE)
		
		propertyName = Word(alphanums+"_-.").setParseAction(self.prependPropertyToken)
		property = dictOf(propertyName + EQ, value)
		properties = Dict(property)
		
		object << (LBRACE + properties + RBRACE)
		value << (data | object | simpleArray)
		
		dataset = properties.ignore(comment)
		
		#parse it
		result = dataset.parseString(inputText)
		
		#turn it into a JSON-like object
		dict = self.convert_to_dict(result.asList())
		return json.dumps(dict)
		
	
	
	def convert_to_dict(self, inputList):
		dict = {}
		for item in inputList:
			#determine the key and value to be inserted into the dict
			dictval = None
			key = None
			
			if isinstance(item, list):
				try:
					key = item[0].replace("__property__","")
					if isinstance(item[1], list):
						try:
							if item[1][0].startswith("__property__"):
								dictval = self.convert_to_dict(item)
							else:
								dictval = item[1]
						except AttributeError:
							dictval = item[1]
					else:
						dictval = item[1]
				except IndexError:
					dictval = None
			#determine whether to insert the value into the key or to merge the value with existing values at this key
			if key:
				if key in dict:
					if isinstance(dict[key], list):
						dict[key].append(dictval)
					else:
						old = dict[key]
						new = [old]
						new.append(dictval)
						dict[key] = new
				else:
					dict[key] = dictval
		return dict

	
			
	def prependPropertyToken(self,t):
		return "__property__" + t[0]
		
	