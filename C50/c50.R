#! /usr/bin/Rscript

library(C50)
library(data.table)
library(pracma)

url <- '../data/train.dat'
#url <- '../data/train_NN.dat'
dat <- read.table( file=url, header=TRUE, sep=",", strip.white=TRUE)

submit = FALSE

if(!submit){
	print(tail( dat, 2 ))
	n_crossval = 40
	ERR		= rep(0,n_crossval)
	ERR_C0	= rep(0,n_crossval)
	ERR_C1	= rep(0,n_crossval)
	#trs		= round(logspace(0, 2, n = 10))
	#trs		= round(linspace(1, 20, n = 20))
	#fzts		= c(FALSE, TRUE)
	#sbs		= c(FALSE, TRUE)
	#print(trs)
	prns		= c(TRUE, FALSE)
	for(prn in prns){
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
			
			tr = 100

			contr = C5.0Control(noGlobalPruning=prn); # default subset
			#contr = C5.0Control(subset=s);
			model <- C50::C5.0( trainX, trainy, control = contr, trials=tr, earlyStopping=FALSE)
			
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
	}
	mean_total	= mean(ERR)
	mean_c0		= mean(ERR_C0)
	mean_c1		= mean(ERR_C1)
	
	print(paste('Correct_total mean: ',mean_total))
	print(paste('Correct_c0 mean:    ',mean_c0))
	print(paste('Correct_c1 mean:    ',mean_c1))

	error_table = data.table(e_total = ERR, e_c0 = ERR_C0, e_c1 = ERR_C1)
	#fname = paste("results/trials_",tr,"_subsets_","TRUE","_fuzzy_",fzt,".dat",sep='')
	#fname = paste("results/trials_",tr,"_subsets_",sb,".dat",sep='')
	fname = paste("results/trials_",tr,"_globalpruning_",prn,".dat",sep='')
	print(fname)
	write.table( error_table, fname, quote=FALSE, sep="," )
	}

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
		if(predictions[i]=='-'){
			write(paste(i,'0',sep=','),fname,append= TRUE)
		}else{
			write(paste(i,'1',sep=','),fname,append= TRUE)
		}
	}
	
	
}
