# corpus_test.py
# experiment to test language identification on fixed corpus

# libraries
import random_idx
import utils
import sys
import scipy.io as scio
import numpy as np
import glob
import os
from tqdm import trange

# important directories
main_base = os.getcwd()
test_dir = '/lang_texts/test/processed_test'

# parameters
N = 10000 # dimension of random index vectors
k = 5000 # number of + (or -)
cluster_min = 3
cluster_max = 3 # size of max letter cluster
ordy = [1]
lang_map = {'af':'afr','bg':'bul','cs':'ces','da':'dan','nl':'nld','de':'deu','en':'eng','et':'est','fi':'fin','fr':'fra','el':'ell','hu':'hun','it':'ita','lv':'lav','lt':'lit','pl':'pol','pt':'por','ro':'ron','sk':'slk','sl':'slv','es':'spa','sv':'swe'}
#lang_map = {'af':'afrikaans','bg':'bulgarian','cs':'czech','da':'danish','nl':'dutch','de':'german','en':'english','et':'estonian','fi':'finnish','fr':'french','el':'greek','hu':'hungarian','it':'italian','pl':'polish','pt':'portuguese','ro':'romanian','sk':'slovak','sl':'slovenian','es':'spanish','sv':'swedish'}
languages = lang_map.values()
#languages = ['french','italian','finnish','estonian']

total_vectors = []


###############################
# generate random indexing for letters, reused throughout
cluster_sizes = xrange(cluster_min,cluster_max+1)
RI_letters = random_idx.generate_letter_id_vectors(N,k)

##############################
# iterate over cluster sizes for language vectors ONLY
for cluster_sz in cluster_sizes:
		for ordered in ordy:

					print "~~~~~~~~~~"
					# calculate language vectors
					lang_vectors = random_idx.generate_RI_lang(N, RI_letters, cluster_sz, ordered, languages=languages)
					total_vectors.append(lang_vectors)

					# print cosine angles 
					print '=========='
					if ordered == 0:
							ord_str = 'unordered!'
					else:
							ord_str = 'ordered!'

					print 'N = ' + str(N) + '; k = ' + str(k) + '; letters clusters are ' + str(cluster_sz) + ', ' + ord_str + '\n'
					cosangles = utils.cosangles(lang_vectors, languages)
					variance = utils.var_measure(cosangles)
					print "variance of language values: " + str(utils.var_measure(cosangles))
final_lang = sum(total_vectors)

###############################
# iterate through test files and calculate correctness
test_fn = glob.glob(main_base + test_dir + '/*txt')
total = len(test_fn)
correct = 0

for i in trange(total):
		testf = test_fn[i]
		unknown_tots = []
		#print len(testf),testf[91:93]
	#if testf == main_base + test_dir + '/da_432_p.txt':
		for cluster_sz in cluster_sizes:
				for ordered in ordy:
						#print testf[71:]
						# calculate unknown vector
						unknown_vector = random_idx.generate_RI_text(N, RI_letters, cluster_sz, ordered,testf)
						unknown_tots.append(unknown_vector)
		final_unknown = sum(unknown_tots)
		likely_lang = utils.find_language(testf, final_unknown, final_lang, languages,display=0)
		#print testf[91:], '=> ',likely_lang
		if lang_map[testf[91:93]] == likely_lang:
				correct +=1

print "correct: ", correct, "; total: ", total,"; final percentage correct: ", float(correct)/total
