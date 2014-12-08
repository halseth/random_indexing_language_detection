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
import matplotlib.pyplot as plt
import networkx as nx

# constants
whitespace = string.whitespace


def load_text(text_name):
		# loads text of text_name, assumes text has .txt and the file exists
		try:
				print 'loading ' + str(text_name)
				textfile = open(text_name)
				text = textfile.read()
				text = text.translate(None,whitespace)
				textfile.close()
		except UnboundLocalError:
				print 'sorry, no such file named ' + text_name

		return text

def load_text_spaces(text_name):
		# loads text of text_name, assumes text has .txt and the file exists
		try:
				print 'loading ' + str(text_name)
				textfile = open(text_name)
				text = textfile.read()
				text = text.translate(None,whitespace[0:-1])
				textfile.close()
		except UnboundLocalError:
				print 'sorry, no such file named ' + text_name

		return text

# The cosine of two vectors
def vector_cosine(a,b):
	a_norm = a / np.linalg.norm(a)
	b_norm = b / np.linalg.norm(b)
	return a_norm.dot(b_norm)

def cosangles(lang_vectors,languages,display=0):
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
		if display:

				# calculate angles
				acos_angles = np.arccos(cos_angles)
				acos_angles[np.isnan(acos_angles)] = 0
				acos_angles[acos_angles < 1e-5] = 0

				display_graph(acos_angles, languages)
		return cos_angles

def display_graph(similarity, languages):
		# display network of languages

		num_lang = len(languages)
		offset=0.07
		dt = [('len',float)]
		similarity = similarity.view(dt)

		G = nx.from_numpy_matrix(similarity)
		G = nx.relabel_nodes(G, dict(zip(range(len(G.nodes())),languages)))
		nx.draw_graphviz(G,prog='neato',alpha=0.5,with_labels=True)
		plt.show()


def find_language(text_name, text_vector, lang_vectors, languages):

		# number of languages
		num_lang,N = lang_vectors.shape

		# normalize language vectors
		lang_vectors_normd = np.zeros(lang_vectors.shape)
		for i in xrange(num_lang):
				lang_vectors_normd[i,:] = lang_vectors[i,:]/np.linalg.norm(lang_vectors[i,:])

		# normalize text vector
		text_vector_normd = text_vector/np.linalg.norm(text_vector)

		cos_angles = lang_vectors_normd.dot(text_vector_normd.T)
		cola = zip(cos_angles,languages)
		cola.sort()
		cola.reverse()
		cos_angles = [x for x,y in cola]
		languages = [y for x,y in cola]
		labeled_cosangles = pd.DataFrame(cos_angles, index=languages, columns=['likelihood'])
		print labeled_cosangles

		likely_lang_idx = np.argmax(cos_angles)
		likely_language = languages[likely_lang_idx]
		print 'most likely language of ' + text_name + ' is ' + str(likely_language)
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

def var_measure(cos_angles):
		num_lang = cos_angles.shape[0]
		iu1 = np.triu_indices(num_lang,1)
		values = np.arcsin(cos_angles[iu1])
		return np.var(values)
