# random_idx.py
# creates random index vectors for a number of languages

# libraries
import sys
import numpy as np
import string
import utils
import pandas as pd

alphabet = string.lowercase

def generate_id(N,k,alph=alphabet,cluster_sz=1):
		# generate id vectors of clusters from "alphabet" with size "cluster_sz"

		# generate clusters
		clusters = utils.generate_unordered_clusters(alph,cluster_sz=cluster_sz)

		M = len(clusters) # number of letter clusters
		num_letters = len(alphabet)

		# build row-wise k-sparse random index matrix
		# each row is random index vector for letter
		RI_letters = np.zeros((num_letters,N))
		for i in xrange(num_letters):
				rand_idx = np.random.permutation(N)
				RI_letters[i,rand_idx[0:k]] = 1
				RI_letters[i,rand_idx[k:2*k]] = -1

		RI = np.zeros((M,N))
		for i in xrange(M):
				# calculate repeats
				cluster = clusters[i]
				first = cluster[0]
				repeats = 0
				for char in cluster:
						if first == char:
								repeats += 1

				if repeats == len(cluster):
						# check if cluster all same letter
						letter_idx = alphabet.find(first)
						#print first, RI_letters[letter_idx,:]
						RI[i,:] = RI_letters[letter_idx,:]
				else:
						letters = list(cluster)
						prod = np.ones((1,N))
						for letter in letters:
								letter_idx = alphabet.find(letter)
								prod = np.multiply(prod, RI_letters[letter_idx,:])
						RI[i,:] = prod
		return clusters, RI

def generate_RI_text(clusters, RI, text_name):
		# generate RI vector for "text_name"
		# assumes text_name has .txt

		text = utils.load_text(text_name)
		for char_num in xrange(len(lang_text)):

				if char_num < cluster_sz:
						continue
				else:
						# build cluster
						cluster = ''
						for j in xrange(cluster_sz):
								cluster = lang_text[char_num - j] + cluster
						if cluster in clusters:
								cluster_idx = clusters.index(cluster)
								lang_vectors[i,:] += RI[cluster_idx,:]
		return text_vector

def generate_RI(clusters, RI, languages=None):

		if languages == None:
				languages = ['english','german','norwegian','finnish']

		N = RI.shape[1] # dimension of random indexing vectors
		cluster_sz = len(clusters[0])
		num_lang = len(languages)

		lang_vectors = np.zeros((num_lang,N))
		for i in xrange(num_lang):

				# load text one at a time (to save mem), English, German, Norwegian
				lang_text = utils.load_lang(languages[i])

				for char_num in xrange(len(lang_text)):

						if char_num < cluster_sz:
								continue
						else:
								# build cluster
								cluster = ''
								for j in xrange(cluster_sz):
										cluster = lang_text[char_num - j] + cluster
								if cluster in clusters:
										cluster_idx = clusters.index(cluster)
										lang_vectors[i,:] += RI[cluster_idx,:]

		return lang_vectors
