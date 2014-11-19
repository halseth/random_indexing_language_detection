# hyperdim.py
# set of experiments using random_idx

# libraries
import random_idx
import utils

N = 1000 # dimension of random index vectors
k = 100 # number of + (or -)
cluster_max = 3 # size of max letter cluster
languages = ['english','german','norwegian','finnish']

total_vectors = []


for cluster_sz in xrange(1,cluster_max+1):

		# generate letter clusters and respective random indexing vectors
		clusters, RI = random_idx.generate_id(N,k,cluster_sz=cluster_sz)

		print "~~~~~~~~~~"
		# calculate language vectors
		lang_vectors = random_idx.generate_RI(clusters, RI, languages=languages)
		total_vectors.append(lang_vectors)
		#unknown_vector = random_idx.generate_RI(clusters, RI)

		# print cosine angles 
		print '=========='
		print 'N = ' + str(N) + '; k = ' + str(k) + '; letters clusters are ' + str(cluster_sz) + '\n'
		cosangles = utils.cosangles(lang_vectors, languages)

final_lang = sum(total_vectors)

print '========='
print 'N = ' + str(N) + '; k = ' + str(k) + '; max size letters clusters are ' + str(cluster_max) + '\n'
cosangles = utils.cosangles(final_lang, languages)

# compare with "unknown text"
