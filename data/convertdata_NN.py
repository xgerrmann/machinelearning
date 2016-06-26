#! /usr/bin/python

import sys
import os
import csv
from colnames import categorical
import numpy as np

def datset2file(datset, header, fname):
	# create output files
	with open(fname,'w+') as file_out:
		# write header
		file_out.write(',\t'.join(header)+'\n')

		for i, data in enumerate(datset):
			# add row numbers (start with 1)
			data_complete = str(i+1)+',\t'+',\t'.join(data)
			# write row to file
			file_out.write(data_complete+'\n')

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
	n_data = len(dataset_categorical)
	n_cols_original = len(dataset_categorical[0])
	categories	= []
	n_cols_bool	= 0
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
	datSet_total = []
	with open(f_train,'rb') as csvfile:
		data = csv.reader(csvfile, delimiter=",")
		for i_row, row in enumerate(data):
			if i_row == 0:
				header = row	# first row is header row
			else:
				datSet_total.append(row[1:]) # remove row indices

	datSet_total = np.array(datSet_total)
	n_train = datSet_total.shape[0]
	n_feat	= datSet_total.shape[1]

	data_train	= datSet_total[:,:(len(datSet_total[0])-1)] # remove last column (contains labels)
	datset_NN	= cat2bool(data_train, categorical)

	fname = 'train_NN.dat'
	datset2file(datset_NN,header,fname)
	
	## convert train data
	datSet_total = []
	with open(f_test,'rb') as csvfile:
		data = csv.reader(csvfile, delimiter=",")
		for i_row, row in enumerate(data):
			if i_row == 0:
				header = row	# first row is header row
			else:
				datSet_total.append(row[1:]) # remove row indices

	datSet_total = np.array(datSet_total)
	n_test	= datSet_total.shape[0]
	n_feat	= datSet_total.shape[1]

	data_test	= datSet_total
	datset_NN	= cat2bool(data_test, categorical)

	fname = 'test_NN.dat'
	datset2file(datset_NN,header,fname)

if __name__ == "__main__":
	main()


