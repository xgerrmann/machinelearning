#! /usr/bin/python

import sys
import os
import csv


def main(argv):
	fname = argv[1]
	print fname
	if not os.path.exists(fname):
		print 'Usage: ./convertdata.py filename.csv'
		sys.exit('File does not exist')
	
	datSet = []
	with open(fname,'rb') as csvfile:
		data = csv.reader(csvfile, delimiter=",")
		for row in data:
			datSet.append(row)
	
	# create output file
	basename = os.path.splitext(fname)[0]
	fname_out = basename+'.dat'
	with open(fname_out,'w+'):
		pass

	# construct header
	n_feat = len(datSet[0])
	header = ','.join('V'+'%d'%(i+1) for i in range(n_feat))

	# write to file
	with open(fname_out,'w+') as file_out:
		#write header:
		file_out.write(header+'\n')

		for i, data in enumerate(datSet):
			# replace 'NaN' with 'NA'
			data = [elem if not elem == 'NaN' else 'NA' for elem in data] # for submission 2 and 3
			# ? is missing data, NA is not available (missing with a cause)
			#data = [elem if not elem == 'NaN' else '?' for elem in data]
			#data = [elem if not elem == 'NaN' else '0' for elem in data]
			#data = [elem if not elem == 'NaN' else '-1' for elem in data]
			# change binary labels to - and +
			# only if data is traindata, testdata has no labels
			if os.path.splitext(fname_out)[0] == 'train':
				if data[-1] == '0':
					data[-1] = '-'
				else:
					data[-1] = '+'
			# add row numbers (start with 1)
			data_complete = str(i+1)+','+','.join(data)
			file_out.write(data_complete+'\n')

if __name__ == "__main__":
	main(sys.argv)

