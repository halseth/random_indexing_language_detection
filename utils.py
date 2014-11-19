# utils.py
# miscallaneous utility functions

# libraries & modules
import sys
import os
import codecs
import string
import pandas as pd
import numpy as np
import itertools

# constants
text_dir = os.getcwd() + '/preprocessed_texts/'
whitespace = string.whitespace


def load_lang(language):
		# loads text in language and removes all spaces

		if language.lower() == 'english':
				print 'loading english text'
				text = load_text('english.txt')
		elif language.lower() == 'german':
				print 'loading german text'
				text = load_text('german.txt')
		elif language.lower() == 'norwegian':
				print 'loading norwegian text'
				text = load_text('norwegian.txt')
		elif language.lower() == 'finnish':
				print 'loading finnish text'
				text = load_text('finnish.txt')
		else:
				print "sorry, no text stored in " + language

		return text

def load_text(text_name):
		# loads text of text_name, assumes text has .txt and the file exists

		textfile = open(text_dir + text_name)
		text = textfile.read()
		text = text.translate(None,whitespace)
		textfile.close()

		return text

def cosangles(lang_vectors,languages):
		# measures the cosine angle of the given "lang_vectors" and labels them with "language"

		# number of languages
		num_lang,N = lang_vectors.shape

		# normalize vectors
		lang_vectors_normd = np.zeros(lang_vectors.shape)
		for i in xrange(num_lang):
				lang_vectors_normd[i,:] = lang_vectors[i,:]/np.linalg.norm(lang_vectors[i,:])

		# cosine angles for similarity!
		cos_angles = lang_vectors_normd.dot(lang_vectors_normd.T)

		# label the cosine angles table
		labeled_cosangles = pd.DataFrame(cos_angles, index=languages, columns=languages)

		print labeled_cosangles
		return cos_angles

def find_language(text_vector, lang_vectors, languages):

		# number of languages
		num_lang,N = lang_vectors.shape

		# normalize language vectors
		lang_vectors_normd = np.zeros(lang_vectors.shape)
		for i in xrange(num_lang):
				lang_vectors_normd[i,:] = lang_vectors[i,:]/np.linalg.norm(lang_vectors[i,:])

		# normalize text vector
		text_vector_normd = text_vector/np.linalg.norm(text_vector)

		cos_angles = lang_vectors_normd.dot(text_vector_normd.T)
		labeled_cosangles = pd.DataFrame(cos_angles, index=languages, columns=['likelihood'])
		print labeled_cosangles

		likely_lang_idx = np.argmax(cos_angles)
		likely_language = languages[likely_lang_idx]
		print 'most likely language of text is ' + str(likely_language)
		return likely_language

def generate_ordered_clusters(alphabet, cluster_sz=1):
		# generates list of letter clusters of size "cluster" with "alphabet", ordered

		cluster_sz -= 1

		if cluster_sz == 0:
				return list(alphabet)

		old_alph = list(alphabet)
		alph = list(alphabet)

		for rep in xrange(cluster_sz):
				new_alph = []
				for i in xrange(len(old_alph)):
						for j in xrange(len(alphabet)):
								new_alph.append(old_alph[i] + alph[j])
				old_alph = new_alph

		return old_alph

def generate_unordered_clusters(alphabet, cluster_sz=1):
		# generate list of letter clusters of size "cluster" with "alphabet", unordered
        
        old_alph = ['']
        while len(old_alph[0]) < cluster_sz:
            new_alph = []
            for s in old_alph:
                for c in alphabet:
                    if len(s)==0 or s[len(s)-1] <= c:
                        new_alph.append(s + c)
            old_alph = new_alph
        return old_alph

def old_generate_unordered_clusters(alphabet, cluster_sz=1):
		# generate list of letter clusters of size "cluster" with "alphabet", unordered

		# generate list of ordered clusters first
		old_alph = generate_ordered_clusters(alphabet, cluster_sz)

		# make faster later
		new_alph = []
		for cluster in old_alph:
				permutations = list(itertools.permutations(cluster,len(cluster)))
				perm_exists = 0
				for i in xrange(len(permutations)):
						perm = ''.join(permutations[i])
						if perm in new_alph:
								perm_exists = 1
				if not perm_exists:
						new_alph.append(cluster)

		return new_alph
