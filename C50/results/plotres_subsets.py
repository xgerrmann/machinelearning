#!/usr/bin/python

import numpy as np
import matplotlib.pyplot as plt

import os
import csv
import glob

# Load data
files = glob.glob('subsets/*.dat')
print files

n_f		= len(files)
std		= np.zeros(shape=(n_f,3))
dat_f	= np.zeros((40,3,2))
labs	= [] 
for i_f, f in enumerate(files):
	base	= os.path.splitext(os.path.basename(f))[0]
	split	= base.split('_')
	setting	= split[-1]
	print setting
	with open(f, 'r') as csvfile:
		spamreader = csv.reader(csvfile, delimiter=',', quotechar='|')
		for i_row, row in enumerate(spamreader):
			if i_row > 0: # skip header row
				dat_f[i_row-1,:,i_f] = row[1:]
	mean	= np.mean(dat_f[:,0,i_f],axis=0)
	std		= np.std(dat_f[:,0,i_f],axis=0)
	print 'Mean: ', mean
	print 'Std:  ', std
	plt.boxplot(dat_f[:,0,i_f],positions=[i_f+1])
	#plt.plot(i_f+1,mean,'or')
	if setting == 'TRUE':
		labs.append('Subsets')
	else:
		labs.append('No subsets')

print dat_f[:,0,0].shape
print(len(dat_f))
plt.xticks([1,2],labs)
plt.ylabel('Error')
plt.title('Effect of the Use of Subsets on the Error')
plt.xlim([0,3])
plt.ylim([0,.25])
plt.savefig('subsets.png')
plt.show()

# conclusion: fuzzy off
