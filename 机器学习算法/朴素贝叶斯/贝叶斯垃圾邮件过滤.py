from naive_bayes import *
def textParse(bigString):
	import re
	listOfTokens = re.split(r'\W*',bigString)
	return [tok.lower() for tok in listOfTokens if len(tok) > 2]
	
def spamTest():
	docList = []
	classList = []
	fullText = []
	for i in range(1,26):
		with open('email/spam/%d.txt'%i,encoding = 'ISO-8859-1') as f1: 
			wordList = textParse(f1.read())
			docList.append(wordList)
			fullText.extend(wordList)
			classList.append(1)
		with open('email/ham/%d.txt'%i,encoding = 'ISO-8859-1') as f2:
			#print(type(f2.read()))
			wordList = textParse(f2.read())
			docList.append(wordList)
			fullText.extend(wordList)
			classList.append(0)
		
	vocabList = createVocabList(docList)
	trainingSet = list(range(50))
	testSet = []
	for i in range(10):
		randIndex = int(random.uniform(0,len(trainingSet)))
		testSet.append(trainingSet[randIndex])
		del(trainingSet[randIndex])
	trainMat = []
	trainClasses = []
	for docIndex in trainingSet:
		trainMat.append(setOfWords2Vec(vocabList,docList[docIndex]))
		trainClasses.append(classList[docIndex])
	p0V,p1V,pSpam = trainNB0(array(trainMat),array(trainClasses))
	errorCount = 0
	for docIndex in testSet:
		wordVector = setOfWords2Vec(vocabList,docList[docIndex])
		if classifyNB(array(wordVector),p0V,p1V,pSpam) != classList[docIndex]:
			errorCount +=1
	print("the error rate is: ",float(errorCount)/len(testSet))
	
#spamTest()