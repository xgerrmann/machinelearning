#!/usr/bin/python

import numpy as np
import matplotlib.pyplot as plt

import os
import csv
import glob

# Load data
files = glob.glob('globalpruning/*.dat')
print files


n_f		= len(files)
mean	= np.zeros(shape=(n_f,3))
std		= np.zeros(shape=(n_f,3))
dat_f	= np.zeros((40,3,2))

for i_f, f in enumerate(files):
	base		= os.path.splitext(os.path.basename(f))[0]
	print base.split('_')
	with open(f, 'r') as csvfile:
		spamreader = csv.reader(csvfile, delimiter=',', quotechar='|')
		for i_row, row in enumerate(spamreader):
			if i_row > 0: # skip header row
				dat_f[i_row-1,:,i_f] = row[1:]
	#mean[i_f]	= np.mean(dat_f,axis=0)
	print np.transpose(np.mean(dat_f,axis=0))
	print np.transpose(np.std(dat_f,axis=0))

#print mean
#print std

# Plot data
#plt.plot(mean+std)

#for i in range(0,3):
#	plt.fill_between([0,1],mean[:,i]+std[:,i],mean[:,i]-std[:,i],alpha=0.5)

print dat_f[:,0,0].shape
print(len(dat_f))
plt.boxplot(dat_f[:,0,:],positions=[2,1])
plt.xticks([1,2],['Global Pruning', 'No Global Pruning'])
plt.ylabel('Error')
plt.title('Effect of Global Pruning on the Classification Error')
#plt.boxplot(dat_f[:,0,1],positions=[1]*40)
plt.savefig('globalpruning.png')

plt.ylim([0,.3])
plt.show()

# conclusion: fuzzy off
