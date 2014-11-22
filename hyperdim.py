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
cluster_max = 3 # size of max letter cluste
ordered_clusters=1
languages = ['english','german','norwegian','finnish','dutch','french','afrikaans','danish','spanish']

total_vectors = []
unknown_tots = []

try:
		unknown_txt = sys.argv[1]
except IndexError:
		unknown_txt = 'unknown1.txt'

for cluster_sz in xrange(3,cluster_max+1):

		# generate letter clusters and respective random indexing vectors
		clusters_RI = random_idx.generate_id(N,k,cluster_sz=cluster_sz, ordered=ordered_clusters)

		print "~~~~~~~~~~"
		# calculate language vectors
		lang_vectors = random_idx.generate_RI_lang(clusters_RI, languages=languages)
		total_vectors.append(lang_vectors)

		# calculate unknown vector
		unknown_vector = random_idx.generate_RI_text(clusters_RI,unknown_txt)
		unknown_tots.append(unknown_vector)

		# print cosine angles 
		print '=========='
		print 'N = ' + str(N) + '; k = ' + str(k) + '; letters clusters are ' + str(cluster_sz) + '\n'
		cosangles = utils.cosangles(lang_vectors, languages)

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
cosangles = utils.cosangles(final_lang, languages, display=1)
