import naive_bayes as bayes
from 贝叶斯垃圾邮件过滤 import *
import feedparser
def calcMostFreq(vocabList,fullText):
	import operator
	freqDict = {}
	for token in vocabList:
		freqDict[token] = fullText.count(token)
		sortedFreq = sorted(freqDict.items(),key = operator.itemgetter(1),reverse = True)
	return sortedFreq[:30]
	
def localWords(feed1,feed0):
	import feedparser
	docList = []
	classList = []
	fullText =[]
	minLen = min(len(feed1['entries']),len(feed0['entries']))
	for i in range(minLen):
		wordList = textParse(feed1['entries'][i]['summary'])
		docList.append(wordList)
		fullText.extend(wordList)
		classList.append(1)
		wordList = textParse(feed0['entries'][i]['summary'])
		docList.append(wordList)
		fullText.extend(wordList)
		classList.append(0)
	vocabList = createVocabList(docList)
	top30Words = calcMostFreq(vocabList,fullText)
	for pairW in top30Words:
		if pairW[0] in vocabList:
			vocabList.remove(pairW[0])
	trainingSet =list( range(2*minLen))
	testSet = []
	for i in range(20):
		randIndex = int(random.uniform(0,len(trainingSet)))
		testSet.append(trainingSet[randIndex])
		del(trainingSet[randIndex])
	trainMat = []
	trainClasses = []
	for docIndex in trainingSet:
		trainMat.append(bagOfWords2VecMN(vocabList,docList[docIndex]))
		trainClasses.append(classList[docIndex])

	p0V,p1V,pSpam = trainNB0(array(trainMat),array(trainClasses))
	errorCount = 0
	for docIndex in testSet:
		wordVector = bagOfWords2VecMN(vocabList, docList[docIndex])
		if classifyNB(array(wordVector),p0V,p1V,pSpam) != classList[docIndex]:
			errorCount += 1	
	print('the error rate is : ',float(errorCount)/len(testSet))
	return vocabList,p0V,p1V
	
		
rs1 = 'http://www.nasa.gov/rss/dyn/image_of_the_day.rss'
rs2 = 'http://www.nasa.gov/rss/dyn/image_of_the_day.rss'
na = feedparser.parse(rs1)
ya = feedparser.parse(rs2)
vocab,pNA,pYA = localWords(ya,na)


	