# nk_experiment.py
# set of experiments using random_idx

# libraries
import random_idx
import utils
import sys
import scipy.io as scio
import numpy as np
import matplotlib.pyplot as plt


languages = ['english','german','norwegian','finnish','dutch','french','afrikaans','danish','spanish']
cluster_sizes = [2,3,4]
ordered = 1 # fixing to ordered clusters only
Ns = [1e3,2e3,3e3,4e3,5e3,6e3,7e3,8e3,9e3,1e4]
sparsities = [0.01, 0.05]#, 0.1, 0.5, 1]
ks = list(np.round((np.logspace(0,4,10))))

#V = np.zeros((len(Ns),len(sparsities)))
V = np.zeros((len(Ns), len(ks)))

# build V (matrix of variances)
for i in xrange(len(Ns)):
		N = int(Ns[i])
		#for j in xrange(len(sparsities)):
		for j in xrange(len(ks)):
				#sparsity = sparsities[j]
				#k = int(N*sparsity/2)
				k = ks[j]
				if k >= N:
						continue
				RI_letters = random_idx.generate_letter_id_vectors(N,k)
				total_vec = []
				print N,k
				print '=========='

				# iterate over ordered vs unordered
				for cluster_sz in cluster_sizes:
						print "~~~~~~~~~~"
						print 'cz = ', cluster_sz
						# calculate language vectors
						lang_vectors = random_idx.generate_RI_lang(N, RI_letters, cluster_sz, ordered, languages=languages)
						total_vec.append(lang_vectors)
						# print cosine angles 
						if ordered == 0:
								ord_str = 'unordered!'
						else:
								ord_str = 'ordered!'

				# calculate total vector
				final_lang = sum(total_vec)

				# calculate variance of cos angle distribution
				cosangles = utils.cosangles(final_lang, languages)
				vary = utils.var_measure(cosangles)
				V[i,j] = vary
				print 'N = ' + str(N) + '; k = ' + str(k) + '; letters clusters are ' + str(cluster_sizes) + ', ' + ord_str + '\n'
				print "variance of cosine values: " + str(vary)
				print '=========='

np.savez('./vars/vars_dump.npz',V=V, Ns=Ns, sparsities=sparsities,ks=ks)

# plot results
#CS = plt.contourf(sparsities,Ns,V, alpha=0.7, cmap=plt.cm.jet)
CS = plt.contourf(np.log10(ks),Ns,V, alpha=0.7, cmap=plt.cm.jet)
CB = plt.colorbar(CS, shrink=0.8, extend='both')
plt.xlabel('log(k)')
plt.ylabel('N')
plt.title('Variance of Cosine Angles Between Vectors')
plt.savefig('./plots/Nk_contours-ridiculous.png',bbox='tight')
plt.show()
