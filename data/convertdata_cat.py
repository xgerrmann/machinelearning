#! /usr/bin/python

import sys
import os
import csv
from colnames import categorical
from datafunctions import dataset2file, changelabels, normalizedata
import numpy as np

def main():
	## Load data
	f_train = 'train.csv'
	f_test	= 'test.csv'

	datSet_total = []
	with open(f_train,'rb') as csvfile:
		data = csv.reader(csvfile, delimiter=",")
		for row in data:
			datSet_total.append(row)
	n_train = len(datSet_total)
	n_feat	= len(datSet_total[0])-1 # last column contains labels

	with open(f_test,'rb') as csvfile:
		data = csv.reader(csvfile, delimiter=",")
		for row in data:
			row.append('?') # ? stands for unknown label
			datSet_total.append(row)
	print 'Features: %d'%n_feat
	# Find uniqe values per column
	n_data = len(datSet_total)
	print 'n_data: %d'%n_data
	print 'n_train: %d'%n_train
	print 'n_test: %d'%(n_data-n_train)

	# construct remapping for number to char via ascii
	remap	= range(97,122+1) # 'a' - 'z'
	tmp_map	= range(65,90+1) # 'A' - 'Z'
	remap.extend(tmp_map)

	datSet_total	= np.array(datSet_total)
	datSet_total	= normalizedata(datSet_total,categorical)
	#max_n = 10
	n_levels = []
	for i in range(n_feat):
		if categorical[i]:
			print 'Feature %d is categorical'%i
		else:
			print 'Feature %d is continuous'%i
		unique_vals = []
		for d in range(n_data):
			#if d>max_n:
			#	break
			elem_cur = datSet_total[d][i]
			if elem_cur == 'NaN' or elem_cur == 'nan':
				datSet_total[d][i] = 'NA' # use ?
				#datSet_total[d][i] = '0' # use ? (perform after normalization)
				continue
			elif categorical[i]:
				if elem_cur not in unique_vals:
					unique_vals.append(elem_cur)
				index = unique_vals.index(elem_cur)
				if index > len(remap)-1:
					sys.exit('Too many unique values')
				datSet_total[d][i] = chr(remap[index])
			elem_new = datSet_total[d][i]
		n_levels.append([len(unique_vals)])
			#print '%s -> %s'%(elem_cur, elem_new)

	## Split data again in test and train data
	datSet_train	= datSet_total[:n_train]
	datSet_test		= datSet_total[n_train:]

	for i_Set, Set in enumerate([datSet_train, datSet_test]):
		
		if i_Set == 0:
			fname = f_train
			Set = changelabels(Set,('0','1'),('-','+'))
		else:
			fname = f_test
		
		# create output files
		basename	= os.path.splitext(fname)[0]
		fname_out	= basename+'.dat'
		dataset2file(Set,[],fname_out)

if __name__ == "__main__":
	main()


