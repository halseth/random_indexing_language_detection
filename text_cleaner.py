#!/usr/bin/python
# -*- coding: UTF-8 -*-
import sys
import string
import codecs
import re

from unidecode import unidecode

include = string.lowercase
exclude = string.punctuation

if(len(sys.argv) < 3):
    print "Usage: python script.py <inputFile.txt> <outputFile.txt>"
    exit()

inputFile = codecs.open(str(sys.argv[1]), encoding='utf-8')
outputFile = open(str(sys.argv[2]), 'w')

for s in inputFile:
		# fixed latin letter mappings
		s = re.sub(u'ø', 'oe', s)
		s = re.sub(u'å', 'aa', s)
		s = re.sub(u'æ', 'ae', s)
		s = re.sub(u'ä', 'ae', s)
		s = re.sub(u'ö', 'oe', s)
		s = re.sub(u'ü', 'ue', s)
		s = re.sub(u'ß', 'ss', s)

		# decode the rest
		s = unidecode(s)

		string_split = s.split()
		new_s = ''

		# check for all uppercase
		for word in string_split:
				for ch in include:
						lowercase_exist = 0
						if ch in word:
								lowercase_exist = 1
								break
				num_exist = 0
				for num in '0123456789':
						if num in word:
								num_exist = 1
				if lowercase_exist and not num_exist:
						new_s += word + ' '
				else:
						new_s += ' '

		# make all letters lowercase
		new_s = new_s.lower()

		# remove punctuation
		t = ''.join(ch for ch in new_s if ch not in exclude)
		outputFile.write(t+'\n')
    
inputFile.close()
outputFile.close()
       
