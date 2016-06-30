#!/usr/bin/python

import numpy as np
import matplotlib.pyplot as plt

import os
import csv
import glob

# Load data
files = sorted(glob.glob('trials/*.dat'))
print files

n_f		= len(files)
mean	= np.zeros(shape=(n_f,3))
std		= np.zeros(shape=(n_f,3))
trials	= np.zeros(shape=(n_f,1),dtype=np.int64)
for i_f, f in enumerate(files):
	base		= os.path.splitext(os.path.basename(f))[0]
	print base.split('_')
	n_trials	= base.split('_')[1]
	trials[i_f]	= int(n_trials)
	with open(f, 'r') as csvfile:
		spamreader = csv.reader(csvfile, delimiter=',', quotechar='|')
		dat_f = np.zeros((40,3))
		for i_row, row in enumerate(spamreader):
			if i_row > 0: # skip header row
				dat_f[i_row-1,:] = row[1:]
		mean[i_f]	= np.mean(dat_f,axis=0)
		std[i_f,:]	= np.std(dat_f,axis=0)


print mean
print std

# Plot data
#plt.plot(mean+std)
trials = np.sort(trials,axis=0)
print trials
trials = np.reshape(trials,(n_f,))
print np.array([1,2,3,4,5,6,7]).shape

colors = ['r','g', 'b']
for i in range(0,3):
	plt.fill_between(trials,mean[:,i]+std[:,i],mean[:,i]-std[:,i],alpha=0.5, color=colors[i])
	plt.plot(trials,mean[:,i], color=colors[i])

plt.ylim([0,1])
plt.xlabel('Trials')
plt.ylabel('Classification Error')

plt.title('Classification Error vs. Number of Boosting Trials')
plt.legend(['Total', 'Class 0', 'Class 1'])
plt.savefig('boosting.png')
plt.show()
