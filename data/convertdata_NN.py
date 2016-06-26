#! /usr/bin/python

import sys
import os
import csv
from colnames import categorical
import numpy as np
from datafunctions import dataset2file

def cat2bool(dataset_categorical,is_categorical):
# This function takes a dataset(np array) where the categories are
# character formatted and converts it to a dataset where
# each seperate category for each feature is converted to a boolean column
# IMPORTANT: this function takes a list with pure data vectors with the same length,
#	thus no headers or index columns!!
# It also take a vector as argument in which the categorical columns are indicated
# the othe columns are left intact

# This new dataset can then be used for usage neural networks.

	# find the (number of) unique values for each category
	n_data			= len(dataset_categorical)
	n_cols_original	= len(dataset_categorical[0])
	categories		= []
	n_cols_bool		= 0
	for i in range(len(is_categorical)):
		cats = np.array([])
		if is_categorical[i]:
			for elem in dataset_categorical[:,i]:
				if elem not in cats and not elem == 'NA':
					cats = np.append(cats,elem)
					n_cols_bool += 1
				#elif elem == 'NA':
				#	sys.exit('Data contains missing data')
		categories.append(cats)

	# construct empty dataset
	n_cols_regular	= len(is_categorical) - sum(is_categorical)
	n_cols_bool		= n_cols_bool
	n_cols = n_cols_regular + n_cols_bool
	dataset_converted = np.zeros((n_data,n_cols),dtype = np.object_)

	# fill dataset
	index_col = 0
	for i in range(n_cols_original):
		# select current column from the dataset
		data_cur = dataset_categorical[:,i]
		# copy data directly for non categorical features
		print i
		if not is_categorical[i]:
			dataset_converted[:,index_col] = data_cur
			index_col += 1
		else:
			n_cats = len(categories[i])
			for c in range(n_cats):
				col_bool = data_cur == categories[i][c]
				dataset_converted[:,index_col] = col_bool.astype(np.string_)
				index_col += 1
	return dataset_converted

def main():
	# load the data
	f_train = 'train.dat'
	f_test	= 'test.dat'
	
	## convert train data
	datSet_total= []
	n_train		= 0
	with open(f_train,'rb') as csvfile:
		data = csv.reader(csvfile, delimiter=",")
		for i_row, row in enumerate(data):
			if i_row == 0:
				header = row	# first row is header row
			else:
				datSet_total.append(row[1:]) # remove row indices
				n_train += 1

	
	with open(f_test,'rb') as csvfile:
		data = csv.reader(csvfile, delimiter=",")
		for i_row, row in enumerate(data):
			# assume same header, thus skip first row
			if i_row>0:
				datSet_total.append(row[1:]) # remove row indices

	datSet_total= np.array(datSet_total)
	
	dataX	= datSet_total[:,:-1]	# data
	datay	= datSet_total[:,-1]	# labels
	datay	= datay.reshape((len(datay),1))

	dataX	= cat2bool(dataX, categorical)
	print dataX[:10,:]
	
	fname_train	= 'train_NN.dat'
	fname_test	= 'test_NN.dat'
	print dataX.shape
	print datay.shape
	data_train	= np.hstack((dataX[:n_train,:],datay[:n_train]))
	data_test	= np.hstack((dataX[n_train:,:],datay[n_train:]))
	print data_train.shape
	print data_test.shape
	dataset2file(data_train,[],fname_train)
	dataset2file(data_test,[],fname_test)

if __name__ == "__main__":
	main()


