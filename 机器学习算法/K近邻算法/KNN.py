from numpy import *
import operator

from pip._vendor.distlib.compat import raw_input


def creat_data_set():
    group = array([[1.0, 1.1], [1.0, 1.0], [0, 0], [0, 0.1]])
    labels = ['A', 'A', 'B', 'B']
    return group, labels


def kNN_classify(inX,dataSet,labels,k):#kNN分类算法实现
    dataset_size = dataSet.shape[0]
    diffMat = tile(inX, (dataset_size,1)) - dataSet
    square_diffMat = diffMat**2
    squareDistance = square_diffMat.sum(axis=1)
    distances = squareDistance**0.5
    sortedDistIndicies = distances.argsort()
    classCount={}
    for i in range(k):
       voteIlabel = labels[sortedDistIndicies[i]]
       classCount[voteIlabel] = classCount.get(voteIlabel,0)+ 1
    sortedClassCount = sorted(classCount.items(),key=operator.itemgetter(1),reverse=True)
    return sortedClassCount[0][0]

def file2matrix(filename):
    fl = open(filename)
    arrayOfLines = fl.readlines();#将文本文件分解为每行数据构成的数组
    numberOfLines = len(arrayOfLines)#行数
    returnMat = zeros((numberOfLines,3))#创建一个numberOfLines * 3零矩阵
    classLabelVector = []#标签向量
    index=0
    for line in arrayOfLines:
        line = line.strip()#去掉空格
        listFromLine = line.split('\t')#根据制表符划分行
        returnMat[index,:] = listFromLine[0:3]
        classLabelVector.append(int(listFromLine[-1]))
        index +=1
    fl.close()
    return returnMat,classLabelVector

def autoNorm(dataSet):
    minVals = dataSet.min(0)
    maxVals = dataSet.max(0)
    ranges = maxVals - minVals
    normDataSet = zeros(shape(dataSet))
    m = dataSet.shape[0]
    normDataSet = dataSet - tile(minVals, (m,1))
    normDataSet = normDataSet / tile(ranges,(m,1))
    return normDataSet, ranges,minVals

def datingClassTest():
    hoRatio = 0.10
    datingDataMat, datingLabels = file2matrix('datingTestSet2.txt')
    norMat, ranges, minVals = autoNorm(datingDataMat)
    m = norMat.shape[0]
    numTestVecs = int(m*hoRatio)
    errorCount = 0.0
    for i in range(numTestVecs):
        classifierResult = kNN_classify(norMat[i,:], norMat[numTestVecs:m,:],datingLabels[numTestVecs:m],3)
        print("The classifier came back with : %d, the real answer is : %d" % (classifierResult, datingLabels[i]))
        if (classifierResult != datingLabels[i]):
            errorCount += 1.0
    print("The total error rate is : %f " %(errorCount / float(numTestVecs)))

def classifyPerson():
    resultList = ['no at all ', 'in small does', 'in large does']
    percentTats = float(raw_input("percentage of time spent playing video games? "))
    ffmiles = float(raw_input("frequent filer miles earned per year? "))
    iceCream = float(raw_input("liters of ice cream  consumed per year? "))
    datingDataMat, datingLabels = file2matrix('datingTestSet2.txt')
    normMat,ranges, minVals = autoNorm(datingDataMat)
    inArr = array([ffmiles, percentTats, iceCream])
    classifierResult = kNN_classify((inArr - minVals) / ranges,normMat,datingLabels, 3)
    print("You wil probably like this person: "+resultList[classifierResult - 1])