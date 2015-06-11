# random_idx.py
# creates random index vectors for a number of languages

# libraries
import sys
import numpy as np
import string
import utils
import pandas as pd
import os
from iv_structure.infinite_vectors import Vector

alphabet = string.lowercase + " "
lang_dir = './preprocessed_texts/'

cluster_cache = {}

def generate_letter_id_vectors(N, k, alph=alphabet):
	# build row-wise k-sparse random index matrix
	# each row is random index vector for letter
	num_letters = len(alphabet)
	RI_letters = {} #np.zeros((num_letters,N))
	for i in xrange(num_letters):
            RI_letters[int(i)] = Vector(N=N,beta=np.exp(1))
	return RI_letters

def id_vector(N, cluster, alphabet, RI_letters,ordered=0):
        if cluster == '':
                        return 0
        if ordered == 0:
                # unordered clusters
                cluster = ''.join(sorted(cluster))

#if it's already calculated, just return it
        if cluster in cluster_cache:
                return cluster_cache[cluster]
                
        vector = np.zeros(N)
        first = cluster[0]
        repeats = 0
        for char in cluster:
                        if first == char:
                                        repeats += 1

        if repeats == len(cluster):
                        # check if cluster all same letter
                        letter_idx = alphabet.find(first)
                        #print first, RI_letters[letter_idx,:]
                        vector = RI_letters[letter_idx]
        else:
                        
                                        # letters = list(cluster)
# 					prod = np.ones((1,N))
# 					for letter in letters:
# 							letter_idx = alphabet.find(letter)
# 							prod = np.multiply(prod, RI_letters[letter_idx,:])
# 					vector = prod
                        
                        # ordered clusters
                        letters = list(cluster)
                        prod = Vector(N=N, beta=np.exp(1),empty=1)#np.ones((1,N))
                        roller = len(letters)-1
                        for letter in letters:
                                        # working code
                                        #letter_idx = alphabet.find(letter)
                                        #prod = np.multiply(prod, RI_letters[letter_idx,:])
                                        #prod = np.roll(prod,1)
                                        
                                        # testing permutations
                                        letter_idx = alphabet.find(letter)
                                        #prod = np.multiply(prod, np.roll(RI_letters[letter_idx, :],roller))
                                        prod = prod.mult(RI_letters[letter_idx].permute(roller))
                                        roller -= 1
                        vector = prod

        if len(cluster_cache) > 100000:
                cluster_cache.clear()
                print "clearing cache"
        cluster_cache[cluster] = vector
        return vector

def generate_RI_str(N, RI_letters, cluster_sz, ordered, string, alph=alphabet):
		# generate RI vector for "text_name"
		# assumes text_name has .txt

		text_vector = np.zeros((1,N))
		for char_num in xrange(len(string)):

				if char_num < cluster_sz:
						continue
				else:
						# build cluster
						cluster = ''
						for j in xrange(cluster_sz):
								cluster = string[char_num - j] + cluster
						text_vector += id_vector(N, cluster, alph,RI_letters, ordered)
		return text_vector
	

def generate_RI_text(N, RI_letters, cluster_sz, ordered, text_name, alph=alphabet):
		# generate RI vector for "text_name"
		# assumes text_name has .txt

		text_vector = Vector(N=N, beta=np.exp(1),empty=0)#np.zeros((1, N))
		text = utils.load_text_spaces(text_name)
		for char_num in xrange(len(text)):

				if char_num < cluster_sz:
						continue
				else:
						# build cluster
						cluster = ''
						for j in xrange(cluster_sz):
								cluster = text[char_num - j] + cluster
						text_vector += id_vector(N, cluster, alph,RI_letters, ordered)
		return text_vector
	
def generate_RI_sentence(N, RI_letters, cluster_sz, ordered, text, alph=alphabet):
		# generate RI vector for "text_name"
		# assumes text_name has .txt

		text_vector = np.zeros((1, N))
		##text = utils.load_text_spaces(text_name)
		for char_num in xrange(len(text)):

				if char_num < cluster_sz:
						continue
				else:
						# build cluster
						cluster = ''
						for j in xrange(cluster_sz):
								cluster = text[char_num - j] + cluster
						text_vector += id_vector(N, cluster, alph,RI_letters, ordered)
		return text_vector
	
	
	#Not really fast. Theoretically faster, but not for real (not using cache)	
def generate_RI_text_fast(N, RI_letters, cluster_sz, ordered, text_name, alph=alphabet):
	text_vector = np.zeros((1, N))
	text = utils.load_text(text_name)
	cluster2 = ''
	vector = np.ones((1,N))
	for char_num in xrange(len(text)):		
		cluster = cluster + text[char_num]
		if len(cluster) < cluster_sz:
			continue
		elif len(cluster) > cluster_sz:
			prev_letter = cluster[0]
			prev_letter_idx = alphabet.find(letter)
			inverse = np.roll(RI_letters[prev_letter_idx,:], cluster_sz-1)
			vector = np.multiply(vector, inverse)
			vector = np.roll(vector, 1)
			letter = text[char_num]
			letter_idx = alphabet.find(letter)
			vector = np.multiply(vector, RI_letters[letter_idx,:])
			cluster = cluster[1:]
		else: # (len(cluster) == cluster_size), happens once
			letters = list(cluster)
			for letter in letters:
				vector = np.roll(vector,1)
				letter_idx = alphabet.find(letter)
				vector = np.multiply(vector, RI_letters[letter_idx,:])
		text_vector += vector
	return text_vector
		
def generate_RI_text_words(N, RI_letters, text_name, alph=alphabet):
		# generate RI vector for "text_name"
		# assumes text_name has .txt

		text_vector = np.zeros((1, N))
		text = utils.load_text_spaces(text_name)
		cluster = ''
		for char_num in xrange(len(text)):
				char = text[char_num]
				if char == ' ':
						text_vector += id_vector(N, cluster, alph, RI_letters)
						# reset cluster
						cluster = ''
				else:
						cluster += text[char_num]
		return text_vector

def generate_RI_text_history(N, RI_letters, text_name, alph=alphabet):
		# generate RI vector for "text_name"
		# assumes text_name has .txt

		text_vector = np.zeros((1, N))
		history_vector = np.zeros((1,N))
		text = utils.load_text(text_name)
		for char_num in xrange(len(text)):
			char = text[char_num]
			letter_idx = alphabet.find(char)
			history_vector = 0.75*history_vector + RI_letters[letter_idx,:]
			text_vector += history_vector	
				
		return text_vector

def generate_RI_lang(N,RI_letters, cluster_sz, ordered, languages=None):

		cluster_cache.clear()

		if languages == None:
				languages = ['english','german','norwegian','finnish']


		num_lang = len(languages)

		lang_vectors = {}#np.zeros((num_lang,N))

		for i in xrange(num_lang):
				# load text one at a time (to save mem), English, German, Norwegian
				print 'loading ' + languages[i]
				lang_vectors[i] = generate_RI_text(N, RI_letters, cluster_sz, ordered, lang_dir + languages[i] + '.txt')

		return lang_vectors


def generate_RI_lang_history(N,RI_letters, languages=None):

		cluster_cache.clear()

		if languages == None:
				languages = ['english','german','norwegian','finnish']


		num_lang = len(languages)

		lang_vectors = np.zeros((num_lang,N))

		for i in xrange(num_lang):
				print 'loading ' + languages[i]
				# load text one at a time (to save mem), English, German, Norwegian
				lang_vectors[i,:] = generate_RI_text_history(N, RI_letters, lang_dir + languages[i] + '.txt')

		return lang_vectors

def generate_RI_lang_words(N, RI_letters, languages=None):

		cluster_cache.clear()

		if languages == None:
				languages = ['english','german','norwegian','finnish']


		num_lang = len(languages)

		lang_vectors = np.zeros((num_lang,N))

		for i in xrange(num_lang):
				print 'loading ' + languages[i]
				# load text one at a time (to save mem), English, German, Norwegian
				lang_vectors[i,:] = generate_RI_text_words(N, RI_letters, lang_dir + languages[i] + '.txt')

		return lang_vectors
