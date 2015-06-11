# utils.py
# miscallaneous utility functions

# libraries & modules
import sys
import os
import codecs
import string
import pandas as pd
pd.set_option('display.height', 1000)
pd.set_option('display.max_rows', 500)
pd.set_option('display.max_columns', 500)
pd.set_option('display.width', 1000)
pd.set_option('precision',3)
import numpy as np
import itertools
import matplotlib as mpl
import matplotlib.pyplot as plt
import networkx as nx
import Table

# date
import time
now = time.strftime("%Y-%m-%d %H:%M")
print now

# constants
whitespace = string.whitespace


def load_text(text_name,display=0):
		# loads text of text_name, assumes text has .txt and the file exists
		try:
				if display:
						print 'loading ' + str(text_name)
				textfile = open(text_name)
				text = textfile.read()
				text = text.translate(None,whitespace)
				textfile.close()
		except UnboundLocalError:
				print 'sorry, no such file named ' + text_name

		return text

def load_text_spaces(text_name,display=0):
		# loads text of text_name, assumes text has .txt and the file exists
		try:
				if display:
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
		lang_vectors_labelled = pd.DataFrame(lang_vectors, index=languages)

		#print labeled_cosangles
		if display:

				# calculate angles
				acos_angles = np.arccos(cos_angles)
				acos_angles[np.isnan(acos_angles)] = 0
				acos_angles[acos_angles < 1e-5] = 0

				display_graph(acos_angles, languages)
		return cos_angles, lang_vectors_labelled

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


def find_language(text_name, text_vector, lang_vectors, languages,display=0):

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
		cos_angles_ord = [x for x,y in cola]
		languages_ord = [y for x,y in cola]
                labeled_cola = pd.DataFrame(cos_angles, index=list(languages), columns=['likelihoods'])
		labeled_cosangles = pd.DataFrame(cos_angles_ord, index=languages_ord, columns=['likelihood'])

		likely_lang_idx = np.argmax(cos_angles)
		likely_language = languages[likely_lang_idx]
		if display:
                                print labeled_cola
                                print "~~~~~~~~~"
				print labeled_cosangles
				print 'most likely match of ' + text_name + ' is ' + str(likely_language)
		return likely_language, cos_angles, languages

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

def disp_confusion_mat(data,row_labels=None,col_labels=None,saven='confusion_matrix',display=0):
    if row_labels == None or col_labels == None:
        print "please provide labels, otherwise visualizing the matrix as a confusion matrix is meaningless"

    df = pd.DataFrame(data, index=row_labels, columns=col_labels)

    with open('./plots/' + saven + '-' + now + '.tex','w') as f:

        f.write('\\documentclass[a4paper,12pt]{article}\n')
        f.write('\\usepackage{booktabs}')
        f.write('\usepackage[a4paper,margin=1in,landscape]{geometry}')
        f.write('\\begin{document}\n')
        f.write('\\begin{table}[ht]\n')
        f.write('\\caption{confusion matrix}')
        f.write('\\centering')
        f.write(df.to_latex())
        f.write('\\end{table}')
        f.write('\end{document}')
