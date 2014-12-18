import os
import sys
import glob

cur_dir = os.getcwd()
test_dir = '/lang_texts/test/unprocessed_test'
output_dir = '/lang_texts/test/processed_test'
files = glob.glob(cur_dir + test_dir + '/*.txt')
for fn in files:
		print fn[72:]
		#print cur_dir + output_dir + fn[72:-4] + '_p.txt'
		os.system("python ./text_cleaner.py " + fn + ' ' + cur_dir + output_dir + fn[72:-4] + '_p.txt')
