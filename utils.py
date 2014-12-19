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
import matplotlib.pyplot as plt
import networkx as nx

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

		#print labeled_cosangles
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
		cos_angles = [x for x,y in cola]
		languages = [y for x,y in cola]
		labeled_cosangles = pd.DataFrame(cos_angles, index=languages, columns=['likelihood'])

		likely_lang_idx = np.argmax(cos_angles)
		likely_language = languages[likely_lang_idx]
		if display:
				print labeled_cosangles
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

def disp_confusion_mat(data,row_labels=None,col_labels=None,save=0,display=0):

		if row_labels == None or col_labels == None:
				print "please provide labels, otherwise visualizing the matrix as a confusion matrix is meaningless"

		# initialize plot 
		fig, ax = plt.subplots()
		fig = plt.gcf()
		heatmap = ax.pcolormesh(data,cmap=plt.cm.Blues,alpha=0.8)
		# put the major ticks at the middle of each cell
		ax.set_xticks(np.arange(data.shape[0]) + 0.5, minor=False)
		ax.set_yticks(np.arange(data.shape[1]) + 0.5, minor=False)
		# want a more natural, table-like display
		ax.invert_yaxis()
		ax.xaxis.tick_top()

		# set labels!!
		ax.set_xticklabels(row_labels,minor=False)
		ax.set_yticklabels(col_labels,minor=False)

		# rotate xlabels stylishly
		plt.xticks(rotation=45)

		ax.grid(False)

		# turn off all ticks
		plt.gca()

		for t in ax.xaxis.get_major_ticks():
				t.tick1On = False
				t.tick2On = False
		for t in ax.yaxis.get_major_ticks():
				t.tick1On = False
				t.tick2On = False

		plt.xlabel('Predicted Labels')
		plt.ylabel('True Labels')
		plt.suptitle('Confusion Matrix')
		plt.axis('tight')
		for y in range(data.shape[0]):
				for x in range(data.shape[1]):
						if np.abs(data[y,x]) <= 1e-4:
								continue

						plt.text(x + 0.5, y + 0.5, '%.1f' % data[y, x],
										 horizontalalignment='center',
										 verticalalignment='center',
										 )
		plt.colorbar(heatmap)

		if save:
				fig.savefig(os.getcwd() + '/plots/confusion_matrix.png')

		if display:
				plt.show()
