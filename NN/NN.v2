#! /usr/bin/Rscript

library(neuralnet)

#url <- '../data/train.dat'
url <- '../data/train_NN.dat'
dat <- read.table( file=url, header=TRUE, sep=",", strip.white = TRUE )
header <- read.table( file=url, nrows=1, header=FALSE, sep=",", strip.white = TRUE )
print(header)
submit = FALSE

if(!submit){
	#print(head( dat, 6 ))
	n_crossval = 1
	ERR		= rep(0,n_crossval)
	ERR_C0	= rep(0,n_crossval)
	ERR_C1	= rep(0,n_crossval)
	
	for(i in 1:n_crossval){
		# shuffle the data
		n_data	<- NROW(dat)
		#n_data
		n_train <- 0.95 * n_data
		#n_train
		dat_shuffle <- dat[sample(n_data),]
		print(head(dat_shuffle))
		# split labels and real data
		n_feat = NCOL(dat_shuffle)-1
		print(n_feat)
		X <- dat_shuffle[,1:n_feat]
		y <- dat_shuffle[,n_feat+1]
		# split test and trainset
		trainX <- X[1:n_train,1:2]
		trainy <- y[1:n_train]
		testX <- X[(n_train+1):n_data,1:2]
		testy <- y[(n_train+1):n_data]
		## add output as last column and also add this to the column names
		traindata <- cbind(trainX, trainy)
		print(colnames(trainX))
		print(head(trainX))
		colnames(traindata) <- c(colnames(trainX), 'output')
		#print(paste(colnames(trainX), collapse='+'))
		# store the expression of variables in a string
		t = paste(colnames(trainX), collapse='+')
		print(t)
		#print(eval(parse(text=t)))
# parsing the string to R is possible with eval and parse
		net.sqrt <- neuralnet( output~eval(parse(text=t)), traindata, hidden = 10, threshold = 0.1)
		print('Finished training')
		
		print(net.sqrt)
		#plot(net.sqrt)
		
		testdata	<- testX
		net.results	<- compute(net.sqrt, testdata)
		print('Finished testing, now outputting results')
		#Lets display a better version of the results
		cleanoutput <- cbind(testdata,testy,
                         as.data.frame(net.results$net.result))
		colnames(cleanoutput) <- c(colnames(testdata),"Expected_Output","NNet_Output")
		print(cleanoutput)
# 		n_c0_test <- sum(testy=='-')
# 		n_c1_test <- sum(testy=='+')
# 		n_c0_test
# 		n_c1_test
# 		correct_total	<- sum( p == testy )/length(p)
# 		
# 		correct_c0		<- sum(as.integer(p[testy=='-'] == testy[testy=='-']))/n_c0_test
# 		correct_c1		<- sum(as.integer(p[testy=='+'] == testy[testy=='+']))/n_c1_test
# 	
# 		ERR[i]		= 1-correct_total
# 		ERR_C0[i]	= 1-correct_c0
# 		ERR_C1[i]	= 1-correct_c1
	}
	
#	mean_total	= mean(ERR)
#	mean_c0		= mean(ERR_C0)
#	mean_c1		= mean(ERR_C1)
#	
#	print(paste('Correct_total mean: ',mean_total))
#	print(paste('Correct_c0 mean:    ',mean_c0))
#	print(paste('Correct_c1 mean:    ',mean_c1))
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
