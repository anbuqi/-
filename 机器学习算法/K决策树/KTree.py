from math import log
import operator
import kTreePlotter
def calShannoEnt(dataset):
	num = len(dataset)
	labelcounts = {}
	for item in dataset:
		currentlabel = item[-1]
		if currentlabel not in labelcounts.keys():
			labelcounts[currentlabel] =0
		labelcounts[currentlabel]+=1
		
	shannoEnt=0.0
	for key in labelcounts:
		prob =  float(labelcounts[key])/num
		shannoEnt -=prob*log(prob,2)
	return shannoEnt
	
def splitDataSet(dataset,axis,value):
	retDataSet = []
	for featVec in dataset:
		if featVec[axis]==value:
			reducedFeatVec = featVec[:axis]
			reducedFeatVec.extend(featVec[axis+1:])
			retDataSet.append(reducedFeatVec)
			
	return retDataSet
	
def creatDataSet():
	dataSet = [[1,1,'yes'],[1,0,'no'],[0,1,'no'],[0,1,'no']]
	labels=['no surfacing','flippers']
	return dataSet,labels
	
def chooseBestFeatureToSplit(dataSet):
	numFeatures = len(dataSet[0])-1
	baseEntropy = calShannoEnt(dataSet)
	bestInfoGain=0.0
	bestFeature=-1
	
	for i in range(numFeatures):
		featList = [example[i] for example in dataSet]
		uniqueVals = set(featList)
		newEntropy = 0.0
		for value in uniqueVals:
			subDataSet = splitDataSet(dataSet,i,value)
			prob = len(subDataSet)/float(len(dataSet))
			newEntropy += prob * calShannoEnt(subDataSet)
			
		infoGain = baseEntropy - newEntropy
		if (infoGain > bestInfoGain):
			bestInfoGain = infoGain
			bestFeature = i
	
	return bestFeature	
	
def majorityCnt(classList):
	classCount = {}
	for vote in classList:
		if vote not in classCount.keys():
			classCount[vote] = 0
		classCount[vote] += 1
	sortedClassCount  =  sorted(classCount.iteritems(),key =  operator.itemgetter(1),reverse = True)
	return sortedClassCount[0][0]
	
def creatTree(dataSet,labels):
	classList = [example[-1] for example in dataSet]
	if classList.count(classList[0]) == len(classList):
		return classList[0]
	if len(dataSet[0]) == 1:
		return majorityCnt(classList)
		
	bestFeat = chooseBestFeatureToSplit(dataSet)
	bestFeatLabel = labels[bestFeat]
	myTree ={bestFeatLabel:{}}
	del(labels[bestFeat])
	featValues = [example[bestFeat] for example in dataSet]
	uniqueVals = set(featValues)
	for value in uniqueVals:
		subLabels = labels[:]
		myTree[bestFeatLabel][value] = creatTree(splitDataSet(dataSet,bestFeat,value),subLabels)
		
	return myTree

def classify(inputTree,featLabels,testVec):
	firstStr = list(inputTree.keys())[0]
	secondDict = inputTree[firstStr]
	featIndex = featLabels.index(firstStr)
	for key in secondDict.keys():
		if testVec[featIndex] == key:
			if 	type(secondDict[key]).__name__ =='dict':
				classLabel = classify(secondDict[key],featLabels,testVec)
			else:
				classLabel = secondDict[key]
				
	return classLabel	
				
				
def storeTree(inputTree, filename):
	import json
	with open(filename,'w') as f:
		json.dump(inputTree,f)

def grabTree(filename):
	import json
	with open(filename) as f:
		return json.load(f)
	
	

myDat,labels=creatDataSet()
#print(myDat)
#print(splitDataSet(myDat,0,1))	
#print(chooseBestFeatureToSplit(myDat)
myTree = kTreePlotter.retrieveTree(0)
print(myTree)
print(classify(myTree,labels,[1,0]))
storeTree(myTree,'classifierStorage.txt')
print(grabTree('classifierStorage.txt'))

