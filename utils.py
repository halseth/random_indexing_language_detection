# utils.py
# miscallaneous utility functions

# libraries & modules
import sys
import os
import codecs
import string

# constants
languages_dir = os.getcwd() + '/preprocessed_texts/'
whitespace = string.whitespace


def load_lang(language):
		# loads text in language and removes all spaces

		if language.lower() == 'english':
				print 'loading english text'
				textfile = open(languages_dir + 'english.txt')
		elif language.lower() == 'german':
				print 'loading german text'
				textfile = open(languages_dir + 'german.txt')
		elif language.lower() == 'norwegian':
				print 'loading norwegian text'
				textfile = open(languages_dir + 'norwegian.txt')
		else:
				print "sorry, no text stored in " + language

		text = textfile.read()
		text = text.translate(None,whitespace)
		textfile.close()

		return text
