#!/bin/bash

# change fn to correct path file as necessary! This is just a template for experiments!!!

for i in 1 2 3 4 5 6
do
	echo "run $i"
	NOW=$(date +"%H-%M-%m-%d-%Y")
	fn="/home/adityajoshi/git/vs265_project_f14/logs/corpus_test_stat-seq-$NOW"

	echo "running corpus test stat"

	#ipython corpus_test_stat.py >  fn
	ipython corpus_test_stat.py 1> $fn
done
