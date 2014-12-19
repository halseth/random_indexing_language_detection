import random_idx
import utils
import numpy as np
import string
import pandas as pd

N = 10000
k = 500
cluster_sz = 2
ordered = 1
alph = string.lowercase + ' '

# generate letter vectors
RI_letters = random_idx.generate_letter_id_vectors(N,k)
RI_letters_n = RI_letters/np.linalg.norm(RI_letters)

# generate english vector
english_vector = random_idx.generate_RI_lang(N, RI_letters, cluster_sz, ordered, languages=['eng'])
normed_eng = english_vector/np.linalg.norm(english_vector)

# generate new string of letters
length = 30
gstr = alph[np.random.randint(len(alph))]
temp_str = gstr

for i in xrange(length):
		max_idx = 0
		maxabs = 0
		for j in xrange(len(alph)):
				temp_str = gstr + alph[j]
				temp_id = random_idx.generate_RI_str(N,RI_letters,cluster_sz,ordered,temp_str)
				#temp_id += 1e1*np.random.randn(1,N)
				temp_id /= np.linalg.norm(temp_id)
				absy = np.abs(temp_id.dot(normed_eng.T))
				#print temp_str, absy
				if absy > maxabs:
						max_idx = j
						maxabs = absy
		gstr += alph[max_idx]
		print len(gstr), maxabs, gstr


'''
for i in xrange(length):
		# find letter vector

		letter_vec = np.ones((1,N))
		for j in xrange(1,cluster_sz+1):
				letter_idx = alph.index(gstr[-j])
				letter_vec *= np.roll(RI_letters[letter_idx,:],j-1)
		letter_vec += 1e-10*np.random.rand(1,N)

		# multiply with english vector
		prod_let = np.multiply(english_vector, letter_vec)
		prod_let_n = prod_let/np.linalg.norm(prod_let)

		# show prod
		proddy = RI_letters_n.dot(prod_let_n.T) #+ RI_letters_n.dot(normed_eng.T)
		proddy_DF = pd.DataFrame(np.abs(proddy), index=list(alph))
		print proddy_DF

		# find letter most similar to product
		nearest = np.argmax(np.abs(proddy))

		# add new letter to total string
		gstr += alph[nearest]
		print gstr
		`print "~~~~~~~~~~~~~~~~"
'''
