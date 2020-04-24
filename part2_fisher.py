import math
import operator
#Dictionary in format: word:(# of minWage, # of lifePart)
#MOVIE STUFF
def readAndPopulateDict(fname):
	with open(fname) as f:
		content=f.readlines()
	for line in content:
		a=line.replace("\n","")
		#split the line into word:count pairs	
		split=a.split(' ')
	
		#print(split)
		#minWage or lifePart and remove the number
		score=int(split[0])
		split.pop(0)

		#go through pairs and assign to dictionary
		for pair in split:
			split2=pair.split(':')
			#print(split2)
			keyword=split2[0]
			occurences=int(split2[1])
			#put the value in dict if not 
			if keyword not in dict:
				if score==1:
					dict[keyword]=(occurences,0)
				else:
					dict[keyword]=(0,occurences)
			#increment the tuple value with #		
			else:
				tempTup=dict[keyword]
				if score==1:
					#del dict[keyword]
					#print (tempTup)
					dict[keyword]=(tempTup[0]+occurences,tempTup[1])
				else:
					dict[keyword]=(tempTup[0],tempTup[1]+occurences)
				
	return dict	

###############################################################################################
#Lecture 13, Slide 28- reference for "smoothing"
#populate dict of multinomial for training set
def populateMultiProb(diction):
	#number of unique words
	minWage=0
	lifePart=0
	#number of words in minWage and lifePart words
	for word in diction:
		temp=diction[word]
		if temp[0]>0:
			minWage=minWage+1
		if temp[1]>0:
			lifePart=lifePart+1
	#print(minWage,lifePart)

	probDict={}
	probDict['wordCountOfReviewsAAA']=(minWage,lifePart)
	
	#Total number of unique words, -1 because wordCountOfReviewsAAA is the
	totWords=len(diction)-1;
	for word in diction:
		temp=diction[word]
		posCount=float(temp[0])
		negCount=float(temp[1])

		posCount=float((posCount+1)/float(minWage+totWords))
		negCount=float((negCount+1)/float(lifePart+totWords))
			
		probDict[word]=(posCount,negCount)
	
	#print(probDict)
	return probDict		

##################################################################################################
#populate dict of bernoulli for training set
def populateBernProb(diction):
	bernDict={}
	
	for words in diction:
		temp=diction[words]
		posCount=float(temp[0])
		#print(posCount)
		negCount=float(temp[1])		
		#Add V, 4000
		posCount=float((posCount+1)/1318)
		#Add V, which is total number of reviews: 4000
		negCount=float((negCount+1)/1316)
	
		bernDict[words]=(posCount,negCount)
	
	return bernDict	

####################################################################################################
#Model 1= Multinomial
#Else Bernoulli
def testStuff(fname,trainingDict,model):
	#remove the word count entry if it was used
	truePos=0
	trueNeg=0
	falsePos=0
	falseNeg=0
	results=[]
	total=len(trainingDict)	
	#Get the count of words from training if necessary
	if model==1:
		temp=trainingDict['wordCountOfReviewsAAA']
		del trainingDict['wordCountOfReviewsAAA']
		positive=float(temp[0])
		negative=float(temp[1])
		#subtract 1 from total because of counter entry
		total=total-1
		
	#read the tester file
	with open(fname) as f:
		content=f.readlines()
	#reading each line
	#print(trainingDict)
	for line in content:
		#parse the lines then check the words
		a=line.replace("\n","")
		#split the line into word:count pairs	
		split=a.split(' ')
		score=int(split[0])
		#remove the first 1/-1 string
		split.pop(0)
		if model==1:
			posProb=float(positive/total)
			negProb=float(negative/total)
		else:
			posProb=float(440.0/878.0)
			negProb=float(438.0/878.0)
		posProb=math.log(posProb)
		negProb=math.log(negProb)
		for pair in split:
			#split the word:number pair and calculate the probability
			split2=pair.split(':')
			#word
			keyword=split2[0]
			#count			
			count=split2[1]
			if keyword in trainingDict:
							
					#print(keyword+" is going to case 1")
					#posCount from populateProb Methods
					posProb=posProb+math.log(float((trainingDict[keyword][0])))
					#print(keyword+" is going to case 2")
					#negCount from populateProb Methods
					negProb=negProb+math.log(float((trainingDict[keyword][1])))
			else:
				if model==1:
				#Multinomial				
						#print(keyword+" is going to case 3")
						newTotal=float((positive+total))					
						posProb=posProb+math.log(float(1/newTotal))
						newTotal2=float((negative+total))
						#print(keyword+" is going to case 4")
						negProb=negProb+math.log(float(1/newTotal2))
				else:
					#print(keyword+" is going to case 5")
					posProb=posProb+math.log(float(1.0/1318))
					negProb=negProb+math.log(float(1.0/1316))

			#print(keyword+" "+str(prob))
			#If test was positive
			if score==1:
				if math.fabs(posProb)<math.fabs(negProb):
					truePos=truePos+1
				else:
					falseNeg=falseNeg+1
			else:
				if math.fabs(posProb)>math.fabs(negProb):
					trueNeg=trueNeg+1
				else:
					falsePos=falsePos+1
		#print posProb, negProb

	acc = float(float(truePos + trueNeg)/float(truePos+falseNeg+trueNeg+falsePos))
	#print truePos, trueNeg, falsePos, falseNeg			
	#print acc
	probDict = {}
	for tup in trainingDict:
		if dict[tup][1] != 0:
			tempProb = float(float(dict[tup][0])/float(dict[tup][1]))
			probDict[tup] = tempProb
	sortedList = sorted(probDict.items(), key=operator.itemgetter(1))
	sortedList.reverse()
	#for i in range(0,10):
	#	print sortedList[i]
	templist = []
	for key,tup in trainingDict.items():
		tempelement = (key, tup)
		templist.append(tempelement)
	templist.sort(key=lambda tup:tup[1][1])
	templist.reverse()
	#for i in range(0,10):
	#	print templist[i]
	for item in sortedList:
		ratio = int(item[1]) + 1
		for i in range(0, ratio):
			print ' '
			print item[0]
####################################################################################################
dict={}
dict=readAndPopulateDict('fisher_train_2topic.txt')
training=populateMultiProb(dict)
training2=populateBernProb(dict)
testStuff('fisher_test_2topic.txt',training,1)
testStuff('fisher_test_2topic.txt',training,0)
#print(dict)


