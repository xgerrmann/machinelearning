#! /usr/bin/Rscript

library(C50)

url <- '../data/train.dat'
#url <- '../data/train_NN.dat'
dat <- read.table( file=url, header=TRUE, sep="," )

submit = FALSE # column are not correct, fix this for NN dataset

if(!submit){
	print(tail( dat, 2 ))
	n_crossval = 1
	ERR		= rep(0,n_crossval)
	ERR_C0	= rep(0,n_crossval)
	ERR_C1	= rep(0,n_crossval)
	
	for(i in 1:n_crossval){
		# shuffle the data
		n_data	= NROW(dat)
		n_feat	= NCOL(dat[1,])-1
		print(n_data)
		print(n_feat)
		n_train <- 0.95 * n_data
		#n_train
		dat_shuffle <- dat[sample(n_data),]

		# split labels and real data
		X <- dat_shuffle[,1:n_feat]
		y <- dat_shuffle[,n_feat+1]
		
		# split test and trainset
		trainX	<- X[1:n_train,]
		trainy	<- y[1:n_train]
		testX	<- X[(n_train+1):n_data,]
		testy	<- y[(n_train+1):n_data]
		
		#model <- C50::C5.0( trainX, trainy )
		#print(paste('Dim trainX: ',dim(trainX)))
		model <- C50::C5.0( trainX, trainy, trials=100)
		#summary( model )
		
		#p <- predict( model, trainX, type="class" )
		p <- predict( model, testX, type="class" )
		
		n_c0_test <- sum(testy=='-')
		n_c1_test <- sum(testy=='+')
		correct_total	<- sum( p == testy )/length(p)
		
		correct_c0		<- sum(as.integer(p[testy=='-'] == testy[testy=='-']))/n_c0_test
		correct_c1		<- sum(as.integer(p[testy=='+'] == testy[testy=='+']))/n_c1_test
	
		ERR[i]		= 1-correct_total
		ERR_C0[i]	= 1-correct_c0
		ERR_C1[i]	= 1-correct_c1
		n_data
		n_train
		print(paste('Correct_total: ',1-correct_total))
		print(paste('Correct_c0:    ',1-correct_c0))
		print(paste('Correct_c1:    ',1-correct_c1))
	}
	
	mean_total	= mean(ERR)
	mean_c0		= mean(ERR_C0)
	mean_c1		= mean(ERR_C1)
	
	print(paste('Correct_total mean: ',mean_total))
	print(paste('Correct_c0 mean:    ',mean_c0))
	print(paste('Correct_c1 mean:    ',mean_c1))
}else{
	## Make submission
	file_train <- '../data/train.dat'
	dat_train	<- read.table( file=file_train, header=TRUE, sep="," )
	
	file_test	<- '../data/test.dat'
	dat_test	<- read.table( file=file_test, header=TRUE, sep="," )
	n_feat	= NCOL(dat_train[1,])-1
	
	dat_test = dat_test[,1:n_feat]
	print(dim(dat_test))
	# split labels and real data
	data	<- dat_train[,1:n_feat]
	labels	<- dat_train[,n_feat+1]
	
	# Train model
	model <- C50::C5.0( data, labels, trials=100 )
	summary( model )
	
	# Make preditions on test data
	predictions <- predict( model, dat_test, type="class" )
	print(predictions)

	# Write to file
	fname <- 'submission.csv'
	write('Id,Prediction',fname)
	
	for(i in 1:length(predictions)){
		#if(predictions[i]=='-'){
		write(paste(i,predictions[i],sep=','),fname,append= TRUE)
		#}else{
		#	write(paste(i,'1',sep=','),fname,append= TRUE)
		#}
	}
	
	
}
