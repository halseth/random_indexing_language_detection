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
import matplotlib.pyplot as plt
import pandas as pd
pd.set_option('precision',2)

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
del lang_map['af'] # no afrikaans in test corpus
lang_tots = lang_map.values()
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
#print final_lang.shape
#langy = final_lang[1,:]
#print langy[:,np.newaxis].shape
#print final_lang[1,:].T.dot(final_lang[1,:]).shape

'''
h,axarr = plt.subplots(len(languages),1)
for i in xrange(len(languages)):
	langy = final_lang[i,:]
	axarr[i].imshow(langy[:,np.newaxis].dot(langy[np.newaxis,:]),cmap='gray',interpolation='nearest')
	axarr[i].set_title(languages[i])
plt.show()
'''

###############################
# iterate through test files and calculate correctness
test_fn = glob.glob(main_base + test_dir + '/*txt')
total = len(test_fn)
correct = 0
guessing_dicts = {}

for i in trange(total):
		testf = test_fn[i]
		unknown_tots = []
		#guesses = {'tag':'','correct':0}
		for cluster_sz in cluster_sizes:
				for ordered in ordy:
						# calculate unknown vector
						unknown_vector = random_idx.generate_RI_text(N, RI_letters, cluster_sz, ordered,testf)
						unknown_tots.append(unknown_vector)
		final_unknown = sum(unknown_tots)
		likely_lang = utils.find_language(testf, final_unknown, final_lang, languages,display=0)

		#print testf[71:], '=> ',likely_lang
		try:
				true_lang = lang_map[testf[71:73]]
		except KeyError:
				continue


		if true_lang not in guessing_dicts.keys():
				guessing_dicts[true_lang] = {'correct':0, 'total':1}
		else:
				guessing_dicts[true_lang]['total'] += 1

		if true_lang == likely_lang:
				correct +=1
				guessing_dicts[true_lang]['correct'] += 1

		if likely_lang not in guessing_dicts[true_lang].keys():
				guessing_dicts[true_lang][likely_lang] = 1
		else:
				guessing_dicts[true_lang][likely_lang] += 1

confusion_matrix = np.zeros((len(lang_map),len(lang_map)))
print "\n"
print "correct: ", correct, "; total: ", total,"; final percentage correct: ", '%.01f' % (100*float(correct)/total)
language_list = guessing_dicts.keys()
for lang in language_list:
		i = lang_tots.index(lang)
		dicty = guessing_dicts[lang]
		#results = ''
		for key in sorted(dicty.keys()):
				if key == 'correct' or key == 'total':
						continue
				j = lang_tots.index(key)
				#results += key + ': %.01f| ' % (dicty[key]/float(dicty['total'])*100)
				confusion_matrix[i,j] = dicty[key]/float(dicty['total'])*100
		#print lang, ': %.01f' % (100*dicty['correct']/float(dicty['total'])), '%:\n\t' + results

utils.disp_confusion_mat(confusion_matrix, row_labels= lang_tots, col_labels = lang_tots,save=1,display=1)
#cm = pd.DataFrame(confusion_matrix, index = lang_tots, columns=lang_tots)
#print cm
#cm.plot(kind='bar', stacked=True);
#plt.show()
