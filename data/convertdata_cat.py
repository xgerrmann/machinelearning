#! /usr/bin/python

import sys
import os
import csv
from colnames import categorical

def main():
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
			datSet_total.append(row)
	#print 'trainset:'
	#print datSet_total[0]

	#print 'testset:'
	#print datSet_total[n_train]

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
	
	#max_n = 10
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
			if elem_cur == 'NaN':
				datSet_total[d][i] = 'NA' # use ? 
				continue
			elif categorical[i]:
				if elem_cur not in unique_vals:
					unique_vals.append(elem_cur)
				index = unique_vals.index(elem_cur)
				if index > len(remap)-1:
					sys.exit('Too many unique values')
				datSet_total[d][i] = chr(remap[index])
			elem_new = datSet_total[d][i]
			#print '%s -> %s'%(elem_cur, elem_new)

	## Split data again in test and train data
	datSet_train	= datSet_total[:n_train]
	datSet_test		= datSet_total[n_train:]
	#print 'trainset:'
	#print datSet_train[0:5]

	#print 'testset:'
	#print datSet_test[0:5]
	
	for i_Set, Set in enumerate([datSet_train, datSet_test]):
		# TODO: use column names
		# construct header
		n_feat = len(Set[0])
		header = ','.join('V'+'%d'%(i+1) for i in range(n_feat))
		
		if i_Set == 0:
			fname = f_train
		else:
			fname = f_test

		# create output files
		basename = os.path.splitext(fname)[0]
		fname_out = basename+'.dat'
		with open(fname_out,'w+') as file_out:
			file_out.write(header+'\n')

			for i, data in enumerate(Set):
				if i_Set == 0:
					# change binary labels to - and +
					# only if data is traindata, testdata has no labels
					if data[-1] == '0':
						data[-1] = '-'
					else:
						data[-1] = '+'
				# add row numbers (start with 1)
				data_complete = str(i+1)+','+','.join(data)
				file_out.write(data_complete+'\n')

if __name__ == "__main__":
	main()
