# hyperdim.py
# set of experiments using random_idx

# libraries
import random_idx
import utils
import sys
import scipy.io as scio
import numpy as np

N = 10000 # dimension of random index vectors
k = 1000 # number of + (or -)
cluster_min = 2
cluster_max = 3 # size of max letter cluste
languages = ['english','german','norwegian','finnish','dutch','french','afrikaans','danish','spanish']

total_vectors = []
unknown_tots = []

try:
		unknown_txt = sys.argv[1]
except IndexError:
		unknown_txt = 'unknown1.txt'

# generate random indexing for letters, reused throughout
cluster_sizes = [3]
cluster_sz = 3
Ns = [1e4,1e5,1e6]
ks = [1e2, 1e3, 1e4]

# iterate over cluster sizes
#for cluster_sz in cluster_sizes:
#for N in Ns:
for k in ks:
		# iterate over whether clusters are/arent ordered
		RI_letters = random_idx.generate_letter_id_vectors(N,k)
		for ordered in [0]:
				# generate letter clusters and respective random indexing vectors
				#clusters_RI = random_idx.generate_id(RI_letters,cluster_sz=cluster_sz, ordered=0)

				print "~~~~~~~~~~"
				# calculate language vectors
				lang_vectors = random_idx.generate_RI_lang(N, RI_letters, cluster_sz, ordered, languages=languages)
				total_vectors.append(lang_vectors)

				# calculate unknown vector
				unknown_vector = random_idx.generate_RI_text(N, RI_letters, cluster_sz, ordered,unknown_txt)
				unknown_tots.append(unknown_vector)

				# print cosine angles 
				print '=========='
				if ordered == 0:
						ord_str = 'unordered!'
				else:
						ord_str = 'ordered!'

				print 'N = ' + str(N) + '; k = ' + str(k) + '; letters clusters are ' + str(cluster_sz) + ', ' + ord_str + '\n'
				cosangles = utils.cosangles(lang_vectors, languages)
				print "variance of upper triangle: " + str(utils.var_measure(cosangles))
'''
final_lang = sum(total_vectors)

# generate language pairs
bilinguals = []
for i in xrange(len(languages)):
		for j in xrange(len(languages)):
				if i < j:
						bilinguals.append((languages[i],languages[j]))
print bilinguals

bilingual_vectors = np.zeros((len(bilinguals),N))
for i in xrange(len(bilinguals)):
		lang1, lang2 = bilinguals[i]

		lang1_idx = languages.index(lang1)
		lang2_idx = languages.index(lang2)

		bilingual_vectors[i,:] = final_lang[lang1_idx,:] + (final_lang[lang2_idx,:])

print '\n'
# compare with "unknown text"
final_unknown = sum(unknown_tots)
utils.find_language(unknown_txt, final_unknown, final_lang, languages)


print '\n'
# compare with "unknown text" on bilinguals
print '========'
utils.find_language(unknown_txt, final_unknown, np.vstack((final_lang, bilingual_vectors)), languages + bilinguals)


print '========='
print 'N = ' + str(N) + '; k = ' + str(k) + '; max size letters clusters are ' + str(cluster_max) + '\n'
cosangles = utils.cosangles(final_lang, languages, display=0)
'''
