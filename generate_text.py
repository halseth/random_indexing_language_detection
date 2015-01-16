import random_idx
import utils
import numpy as np
import string
import pandas as pd

N = 10000
k = 5000
cluster_sz = 2
ordered = 1
#alph = 'abc' 
alph = string.lowercase + ' '

def gen_lets(N=N,k=k):
        # generate letter vectors
        RI_letters = random_idx.generate_letter_id_vectors(N,k)
        RI_letters_n = RI_letters/np.linalg.norm(RI_letters)
        return RI_letters, RI_letters_n


RI_letters, RI_letters_n = gen_lets()
def generate_words(cluster_sz):
        print "generating english vector of cluster size", cluster_sz
        # generate english vector
        english_vector = random_idx.generate_RI_lang(N, RI_letters, cluster_sz, ordered, languages=['eng'])
        #english_vector = random_idx.generate_RI_text_words(N, RI_letters, './lang_texts/texts_english/eng.txt')
        normed_eng = english_vector/np.linalg.norm(english_vector)
        # generate new string of letters
        length = 30
        alphy = utils.generate_ordered_clusters(alph, cluster_sz=cluster_sz)
        gstr = alph[np.random.randint(len(alph))]
        temp_str = gstr
        for i in xrange(length):
                max_idx = 0
                maxabs = 0
        for j in xrange(len(alphy)):
                temp_str = gstr + alphy[j]
                temp_id = random_idx.generate_RI_str(N,RI_letters,cluster_sz,ordered,temp_str)
                #temp_id += 1e1*np.random.randn(1,N)
                temp_id /= np.linalg.norm(temp_id)
                absy = np.abs(temp_id.dot(normed_eng.T))
                #print temp_str, absy
                if absy > maxabs:
                        max_idx = j
                        maxabs = absy
        gstr += alphy[max_idx]
        print len(gstr), maxabs, gstr

def create_english_vec(N=N,k=k):
        print "generating english vector of cluster size", cluster_sz
        # generate english vector
        english_vector = random_idx.generate_RI_lang(N, RI_letters, cluster_sz, ordered, languages=['eng'])
        normed_eng = english_vector/np.linalg.norm(english_vector)
        return english_vector, normed_eng

english_vector, normed_eng = create_english_vec()
blocks = utils.generate_ordered_clusters(alph, cluster_sz=cluster_sz)
#print blocks
RI_blocks = np.zeros((len(blocks),N))
for i in xrange(len(blocks)):
    RI_blocks[i,:] = random_idx.id_vector(N, blocks[i], alph, RI_letters, ordered=ordered)

# testing letter blocks for their "block partners"
test_letter = 's'
letter_idx = alph.index(test_letter)
letter = RI_letters[letter_idx,:]
letter_n = RI_letters[letter_idx,:]
'''
sub_eng = np.copy(english_vector)
for r in xrange(len(blocks)):
    block = blocks[r]
    if test_letter != block[0]:
        sub_eng[:, RI_blocks[r,:] != 0] = 1e-2
print sub_eng
'''

#factored_eng = np.multiply(english_vector, np.roll(letter, 1))
factored_eng = np.multiply(english_vector, np.roll(letter, 1))
#factored_eng = np.roll(np.multiply(english_vector, letter), -1)
#factored_RI_letters = RI_letters, np.roll(letter,1))

likely_block_partner = utils.find_language(test_letter, factored_eng, RI_letters, alph, display=1)

'''
print "ri letters"
for x in xrange(len(alph)):
    print alph[x]
    print RI_letters[x,:]
print "eng vec"
print english_vector
print 'factored eng'
print factored_eng
print 'diff'
print english_vector - factored_eng
'''
'''
# vague attempt at generating text over different parameters
for cz in xrange(1,3+1):
        generate_words(cz)
'''
