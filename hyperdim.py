# hyperdim.py
# set of experiments using random_idx

# libraries
import random_idx
import utils
import sys
import scipy.io as scio

N = 10000 # dimension of random index vectors
k = 100 # number of + (or -)
cluster_max = 2 # size of max letter cluste
ordered_clusters=1
languages = ['english','german','norwegian','finnish','dutch','french','afrikaans','danish','spanish']

total_vectors = []
unknown_tots = []

try:
		unknown_txt = sys.argv[1]
except IndexError:
		unknown_txt = 'unknown1.txt'


for cluster_sz in xrange(1,cluster_max+1):

		# generate letter clusters and respective random indexing vectors
		clusters, RI = random_idx.generate_id(N,k,cluster_sz=cluster_sz, ordered=ordered_clusters)

		print "~~~~~~~~~~"
		# calculate language vectors
		lang_vectors = random_idx.generate_RI_lang(clusters, RI, languages=languages)
		total_vectors.append(lang_vectors)

		# calculate unknown vector
		unknown_vector = random_idx.generate_RI_text(clusters, RI,unknown_txt)
		unknown_tots.append(unknown_vector)

		# print cosine angles 
		print '=========='
		print 'N = ' + str(N) + '; k = ' + str(k) + '; letters clusters are ' + str(cluster_sz) + '\n'
		cosangles = utils.cosangles(lang_vectors, languages)

final_lang = sum(total_vectors)


print '\n'
# compare with "unknown text"
final_unknown = sum(unknown_tots)
utils.find_language(unknown_txt, final_unknown, final_lang, languages)

print '========='
print 'N = ' + str(N) + '; k = ' + str(k) + '; max size letters clusters are ' + str(cluster_max) + '\n'
cosangles = utils.cosangles(final_lang, languages,display=1)
