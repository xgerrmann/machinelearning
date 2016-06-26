#! /usr/bin/Rscript
library(VIM)
library(StatMatch)
library(C50)
library(dprep)

url <- '../data/train.dat'
dat <- read.table( file=url, header=TRUE, sep="," )

n_crossval = 20
ERR		= rep(0,n_crossval)
ERR_C0	= rep(0,n_crossval)
ERR_C1	= rep(0,n_crossval)

for(i in 1:n_crossval){
	# shuffle the data
	n_data	<- nrow(dat)
	#n_data
	n_train <- 0.95 * n_data
	#n_train
	dat_shuffle <- dat[sample(n_data),]
	
	
	#neighbors = 5
	# try maxCat and sampleCat
	# try with and without using imputed values
	#train_knn_imputed = kNN(trainX, variable = colnames(trainX), metric = NULL, k = neighbors,
	#	dist_var = cilnames(Data), weights = NULL numFun = median,
	#	catFun = maxCat, makeNA = NULL, NAcond = NULL, impNA = TRUE,
	#	donorcond = NULL, mixed = vector(), mixed.constant = NULL,
	#	trace = FALSE, imp_var = TRUE, imp_suffix = "imp", addRandom = FALSE,
	#	useImputedDist = FALSE)
	
	# split labels and real data
	print('Dat_shuffle:')
	print(dim(dat_shuffle))
	X <- dat_shuffle[,1:13]
	y <- dat_shuffle[,14]
	
	neighbors = 5
	X_imputed = kNN(X,k = neighbors,trace = TRUE)
	X_imputed = X_imputed[,1:13]
	
	# horizontal concatenation of data
	data_imputed <- cbind(X_imputed,y)
	print('X_imputed:')
	print(dim(X_imputed))

	print('Dat_imputed combined:')
	print(dim(data_imputed))
	#print(dim(data_imputed))
	
	data_train	<- data_imputed[1:n_train,]
	data_test	<- data_imputed[(n_train+1):n_data,]
	testy		<- y[(n_train+1):n_data]
	
	trainX	= data_train[,1:13]
	trainy	= data_train[,14]
	testX	= data_test[,1:13]
	testy	= data_test[,14]
	model <- C50::C5.0( trainX, trainy, trials=100)
	
	p <- predict( model, testX, type="class" )
	print(p)

	n_c0_test <- sum(testy=='-')
	n_c1_test <- sum(testy=='+')
	n_c0_test
	n_c1_test
	correct_total	<- sum( p == testy )/length(p)

	correct_c0		<- sum(as.integer(p[testy=='-'] == testy[testy=='-']))/n_c0_test
	correct_c1		<- sum(as.integer(p[testy=='+'] == testy[testy=='+']))/n_c1_test

	ERR[i]		= 1-correct_total
	ERR_C0[i]	= 1-correct_c0
	ERR_C1[i]	= 1-correct_c1
}

mean_total	= mean(ERR)
mean_c0		= mean(ERR_C0)
mean_c1		= mean(ERR_C1)

print(paste('Error_total mean: ',mean_total))
print(paste('Error_c0 mean:    ',mean_c0))
print(paste('Error_c1 mean:    ',mean_c1))
