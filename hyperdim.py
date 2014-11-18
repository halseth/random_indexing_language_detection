# hyperdim.py
# set of experiments using random_idx

# libraries
import random_idx as RI
import utils

N = 100000 # dimension of random index vectors
k = 1000 # number of + (or -)
cluster = 3 # size of letter cluster
languages = ['english','german','norwegian','finnish']


for cluster in [1, 2, 3]:

		print "~~~~~~~~~~"
		# calculate language vectors
		lang_vectors = RI.generate_vectors(N, k, cluster, languages=languages)

		# print cosine angles 
		print '=========='
		print 'N = ' + str(N) + '; k = ' + str(k) + '; letters clusters are ' + str(cluster) + '\n'
		cosangles = utils.cosangles(lang_vectors, languages)
