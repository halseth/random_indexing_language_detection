# hyperdim.py
# set of experiments using random_idx

# libraries
import random_idx as RI
import utils

N = 100000 # dimension of random index vectors
k = 1000 # number of + (or -)
cluster_max = 3 # size of max letter cluster
languages = ['english','german','norwegian','finnish']

total_vectors = []
for cluster in xrange(1,cluster_max+1):

		print "~~~~~~~~~~"
		# calculate language vectors
		lang_vectors = RI.generate_vectors(N, k, cluster, languages=languages)
		total_vectors.append(lang_vectors)

		# print cosine angles 
		print '=========='
		print 'N = ' + str(N) + '; k = ' + str(k) + '; letters clusters are ' + str(cluster) + '\n'
		cosangles = utils.cosangles(lang_vectors, languages)

final_lang = sum(total_vectors)

print '========='
print 'N = ' + str(N) + '; k = ' + str(k) + '; max size letters clusters are ' + str(cluster) + '\n'
cosangles = utils.cosangles(final_lang, languages)
