#! /usr/bin/Rscript

#url <- "https://archive.ics.uci.edu/ml/machine-learning-databases/credit-screening/crx.data""
#crx <- read.table( file="./crx.dat", header=FALSE, sep="," )
#url <- "https://archive.ics.uci.edu/ml/machine-learning-databases/credit-screening/crx.data"

#library(C50)
#library(rpart)
#library(RWeka)
library(randomForest)

url <- '../train.dat'
dat <- read.table( file=url, header=TRUE, sep="," )

write.table( dat, "tmp.dat", quote=FALSE, sep="," )

submit = FALSE

if(!submit){
	head( dat, 6 )
	n_crossval = 10
	ERR		= rep(0,n_crossval)
	ERR_C0	= rep(0,n_crossval)
	ERR_C1	= rep(0,n_crossval)
	
	for(i in 1:n_crossval){
		print(paste('Iteration: ',i))
		# shuffle the data
		n_data	<- nrow(dat)
		#n_data
		n_train <- 0.95 * n_data
		#n_train
		dat_shuffle <- dat[sample(n_data),]
		
		
		# split labels and real data
		X <- dat_shuffle[,1:13]
		y <- dat_shuffle[,14]
		
		# split test and trainset
		trainX <- X[1:n_train,]
		trainy <- y[1:n_train]
		testX <- X[(n_train+1):n_data,]
		testy <- y[(n_train+1):n_data]
		
		#model <- C50::C5.0( trainX, trainy )
		model <- randomForest( V14~., data=dat, na.action=na.omit)
		#summary( model )
		
		#p <- predict( model, trainX, type="class" )
		p <- predict( model, testX, type="class" )
		#p
		#testy
		#length(trainy)
		#length(testy)
		#length(p)
		#sum( p == trainy )/length(p)
		n_c0_test <- sum(testy=='-')
		n_c1_test <- sum(testy=='+')
		n_c0_test
		n_c1_test
		correct_total	<- sum( p == testy )/length(p)
		#p
		#testy
		correct_c0		<- sum(as.integer(p[testy=='-'] == testy[testy=='-']))/n_c0_test
		correct_c1		<- sum(as.integer(p[testy=='+'] == testy[testy=='+']))/n_c1_test
	
		ERR[i]		= 1-correct_total
		ERR_C0[i]	= 1-correct_c0
		ERR_C1[i]	= 1-correct_c1
		#n_data
		#n_train
		#print(paste('Correct_total: ',1-correct_total))
		#print(paste('Correct_c0:    ',1-correct_c0))
		#print(paste('Correct_c1:    ',1-correct_c1))
	}
	
	mean_total	= mean(ERR)
	mean_c0		= mean(ERR_C0)
	mean_c1		= mean(ERR_C1)
	
	print(paste('Correct_total mean: ',mean_total))
	print(paste('Correct_c0 mean:    ',mean_c0))
	print(paste('Correct_c1 mean:    ',mean_c1))
}else{
	## Make submission
	file_train <- '../train.dat'
	dat_train	<- read.table( file=file_train, header=TRUE, sep="," )
	
	file_test	<- '../test.dat'
	dat_test	<- read.table( file=file_test, header=TRUE, sep="," )
	
	write.table( dat_train, "train_tmp.dat", quote=FALSE, sep="," )
	write.table( dat_test, "test_tmp.dat", quote=FALSE, sep="," )
	
	# Split data (labels and real data)
	data <- dat_train[,1:13]
	labels <- dat_train[,14]
	
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
		if(predictions[i]=='-'){
			write(paste(i,'0',sep=','),fname,append= TRUE)
		}else{
			write(paste(i,'1',sep=','),fname,append= TRUE)
		}
	}
	
	
}
