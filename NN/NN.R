#! /usr/bin/Rscript

library(neuralnet)

#url <- '../data/train.dat'
url <- '../data/train_NN.dat'
dat <- read.table( file=url, header=TRUE, sep=",", strip.white = TRUE )
header <- read.table( file=url, nrows=1, header=FALSE, sep=",", strip.white = TRUE )

submit = FALSE

if(!submit){
	#print(head( dat, 6 ))
	n_crossval = 5
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
		# split labels and real data
		n_feat = NCOL(dat_shuffle)-1
		X <- dat_shuffle[,1:n_feat]
		y <- dat_shuffle[,n_feat+1]
		# split test and trainset
		N_FEAT = 112
		trainX <- X[1:n_train,1:N_FEAT]
		#trainX <- X[1:n_train,]
		trainy <- y[1:n_train]
		testX <- X[(n_train+1):n_data,]
		testy <- y[(n_train+1):n_data]
		trainingdata <- cbind(trainX, trainy)
		
		#colnames(trainingdata) <-c("Input1", "Input2", "Output")
		colnames(trainingdata) <-c(colnames(trainX), "Output")
		t = paste(colnames(trainX),collapse='+')
		t = paste('Output~',t)
		print(t)
		print(parse(text=t))
		#net.sqrt <- neuralnet( Output~V1 + V2, trainingdata, hidden = 10, threshold = 0.1)
		hid		= c(10,10)
		thresh	= 0.1
		lrs		= 1

		net.sqrt <- neuralnet( eval(parse(text=t)), trainingdata, hidden = hid, threshold = thresh)
			
		testdata <- testX[,1:N_FEAT]
		#testdata <- testX
		net.results <- compute(net.sqrt, testdata)
		print(net.results$net.result)
		write.table( cbind(testy,as.data.frame(net.results$net.result)), paste("results/crossval_",i,"-",n_crossval,'_hidden_',hid,'_thresh_',thresh,'_layers_',lrs,'_feat_',N_FEAT,".dat"), quote=FALSE, sep="," )
		#Lets display a better version of the results
		res = as.data.frame(net.results$net.result)
		cleanoutput <- cbind(testdata,testy,
                         as.data.frame(net.results$net.result))
		
		colnames(cleanoutput) <- c(colnames(testdata),"Expected_Output","NNet_Output")
		print(cleanoutput)
		thresh = 0.4
		p = res>thresh
		print(p)
 		n_c0_test <- sum(testy=='0')
 		n_c1_test <- sum(testy=='1')
# 		n_c0_test
# 		n_c1_test
 		correct_total	<- sum( p == testy )/length(p)

 		correct_c0		<- sum(as.integer(p[testy=='0'] == testy[testy=='0']))/n_c0_test
 		correct_c1		<- sum(as.integer(p[testy=='1'] == testy[testy=='1']))/n_c1_test

 		ERR[i]		= 1-correct_total
 		ERR_C0[i]	= 1-correct_c0
 		ERR_C1[i]	= 1-correct_c1
 		print(ERR[i])
 		print(ERR_C0[i])
 		print(ERR_C1[i])
	}
	
	mean_total	= mean(ERR)
	mean_c0		= mean(ERR_C0)
	mean_c1		= mean(ERR_C1)
#	
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
