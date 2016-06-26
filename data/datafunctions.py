import numpy as np

def changelabels(dataset,labels_current, labels_new):
# take a dataset where the last column containts teh labels
# labels_current and labels_new are lists with the same length and contain
# string constants of the old and new labels
	print 'Converting labels'
	# change binary labels to - and +
	# only if data is traindata, testdata has no labels
	for i_lab, lab_cur in enumerate(labels_current):
		# replace labels in last column
		print lab_cur, '->', labels_new[i_lab]
		dataset[(dataset[:,-1]==lab_cur),-1] = labels_new[i_lab]
	return dataset

def dataset2file(dataset, header, fname):
	# TODO: use column names
	# construct header
	n_feat = len(dataset[0])
	header = ('V'+'%d'%(i+1) for i in range(n_feat))
	print header
	# create output file
	with open(fname,'w+') as file_out:
		# write header
		file_out.write(',\t'.join(header)+'\n')

		for i, data in enumerate(dataset):
			# add row numbers (start with 1)
			data_complete = str(i+1)+',\t'+',\t'.join(data)
			# write row to file
			file_out.write(data_complete+'\n')

def normalizedata(datSet,categorical):
	print datSet.shape
	for col, cat in enumerate(categorical):
		if not cat:
			dat_col	= datSet[:,col].astype(np.float)
			val_min	= np.nanmin(dat_col)
			val_max	= np.nanmax(dat_col) - val_min
			dat_col = dat_col - val_min
			dat_col = dat_col/val_max
			datSet[:,col] = dat_col.astype(np.object_)
	return datSet
