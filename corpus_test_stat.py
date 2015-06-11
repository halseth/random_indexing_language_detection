# corpus_test.py
# experiment to test language identification on fixed corpus

# libraries
import random_idx
from tsne import *
import utils
import sys
import scipy.io as scio
import numpy as np
import glob
import os
from tqdm import trange
import time
import matplotlib.pyplot as plt
import pandas as pd
import string
pd.set_option('precision',2)

# constants
now = time.strftime("%Y-%m-%d %H:%M")
print now
alph = string.lowercase + ' '

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


t0 = time.time()
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
					cosangles,lbled_lang_vectors = utils.cosangles(lang_vectors, languages)
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

t1 = time.time()
tt1 = t1- t0
print "time to create " + str(len(languages)) + " language vectors: " + str(tt1)


#t0 = time.time()
################################
## iterate through test files and calculate correctness
#test_fn = glob.glob(main_base + test_dir + '/*txt')
#total = len(test_fn)
#correct = 0
#guessing_dicts = {}
#
#for i in trange(total):
#		testf = test_fn[i]
#		unknown_tots = []
#		#guesses = {'tag':'','correct':0}
#		for cluster_sz in cluster_sizes:
#				for ordered in ordy:
#						# calculate unknown vector
#						unknown_vector = random_idx.generate_RI_text(N, RI_letters, cluster_sz, ordered,testf)
#						unknown_tots.append(unknown_vector)
#		final_unknown = sum(unknown_tots)
#		likely_lang = utils.find_language(testf, final_unknown, final_lang, languages,display=0)
#
#		#print testf[71:], '=> ',likely_lang
#		try:
#				true_lang = lang_map[testf[71:73]]
#		except KeyError:
#				continue
#
#
#		if true_lang not in guessing_dicts.keys():
#				guessing_dicts[true_lang] = {'correct':0, 'total':1}
#		else:
#				guessing_dicts[true_lang]['total'] += 1
#
#		if true_lang == likely_lang[0]:
#				correct +=1
#				guessing_dicts[true_lang]['correct'] += 1
#
#		if likely_lang[0] not in guessing_dicts[true_lang].keys():
#				guessing_dicts[true_lang][likely_lang[0]] = 1
#		else:
#				guessing_dicts[true_lang][likely_lang[0]] += 1
#
#confusion_matrix = np.zeros((len(lang_map),len(lang_map)))
#print "\n"
#print "correct: ", correct, "; total: ", total,"; final percentage correct: ", '%.01f' % (100*float(correct)/total)
#language_list = guessing_dicts.keys()
#for lang in language_list:
#		i = lang_tots.index(lang)
#		dicty = guessing_dicts[lang]
#		#results = ''
#		for key in sorted(dicty.keys()):
#				if key == 'correct' or key == 'total':
#						continue
#				j = lang_tots.index(key)
#				#results += key + ': %.01f| ' % (dicty[key]/float(dicty['total'])*100)
#				confusion_matrix[i,j] = dicty[key]#/float(dicty['total'])*100
#		#print lang, ': %.01f' % (100*dicty['correct']/float(dicty['total'])), '%:\n\t' + results
#
#utils.disp_confusion_mat(confusion_matrix, row_labels= lang_tots, col_labels = lang_tots,display=1)
##cm = pd.DataFrame(confusion_matrix, index = lang_tots, columns=lang_tots)
##print cm
##cm.plot(kind='bar', stacked=True);
##plt.show()
#t1 = time.time()
#tt2 = t1 - t0
#print "creating confusion matrix time: " + str(tt2)


t0 = time.time()
###############################
# dimension reduction plot to view vectors in 2-d


print '========='
print 'N = ' + str(N) + '; k = ' + str(k) + '; max size letters clusters are ' + str(cluster_max) + '\n'
cosangles, _ = utils.cosangles(final_lang, languages, display=0)
print "variance of language values: " + str(utils.var_measure(cosangles))

# plot language points
fig = plt.figure()
Y = tsne(cosangles,no_dims=2,initial_dims=100,perplexity=8)
plt.scatter(Y[:,0],Y[:,1])#,len(languages),np.r_[1:len(languages)])
for label, x, y in zip(languages, Y[:, 0], Y[:, 1]):
    plt.annotate(
        label, 
        xy = (x, y), xytext = (-2, 2),
        textcoords = 'offset points', ha = 'right', va = 'bottom',
        #bbox = dict(boxstyle = 'round,pad=0.5',fc='w'),
        #arrowprops = dict(arrowstyle = '-', 
        #connectionstyle = 'arc3,rad=0.3'),
        fontsize='22')
frame = plt.gca()
frame.axes.get_xaxis().set_ticks([])
frame.axes.get_yaxis().set_ticks([])
plt.savefig(os.getcwd() + '/plots/cosangle_'+ now +'.png')
plt.show()
t1 = time.time()
tt3 = t1 - t0
print "dimension reduction: " + str(tt3)

t0 = time.time()
def find_letter_partner(test_letter, lang_vector):
        # testing letter blocks for their "block partners"
        test_vec = random_idx.id_vector(N,test_letter,alph, RI_letters, ordered=ordered)
        #test_vec = test_vec/np.linalg.norm(test_vec)

        '''
        sub_eng = np.copy(english_vector)
        for r in xrange(len(blocks)):
            block = blocks[r]
            if test_letter != block[0]:
                sub_eng[:, RI_blocks[r,:] != 0] = 1e-2
        print sub_eng
        '''

        cz = len(test_letter)
        #if cz > 1:
        #    for i in xrange(len(alph)):
        #        english_vector -= RI_letters[i,:]
        #english_vector /= np.linalg.norm(english_vector)

        #factored_eng = np.multiply(english_vector, np.roll(letter, 1))
        factored_lang = np.multiply(lang_vector, np.roll(test_vec, 1))
        #factored_eng = np.roll(np.multiply(english_vector, letter), -1)
        #factored_RI_letters = RI_letters, np.roll(letter,1))


        #if len(test_letter) == 1:
        likely_block_partner, values, partners = utils.find_language(test_letter, factored_lang, RI_letters, alph, display=1)
        return likely_block_partner, values, partners

block_list = ['th']
print lbled_lang_vectors[:][1]
lang_vector = np.reshape(lang_vectors[1,:],len(lang_vectors[1,:]),1)

for block in block_list:
    likely_block_partner, values, partners = find_letter_partner(block, lang_vector)

t1 = time.time()
tt4 = t1 - t0
print "finding letter partner time: " + str(tt4)

print "total time of execution: " + str(tt1 + tt2 + tt3 + tt4)
