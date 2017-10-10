import pandas
import math
import numpy

trainData = pandas.read_csv('banknote_train.csv', delimiter=',')
variance = []
skewness = []

# scaling

for i, row in trainData.iterrows():
    variance.append(row[0])
    skewness.append(row[1])

maxV = max(variance)
minV = min(variance)
maxS = max(skewness)
minS = min(skewness)
rangeV = maxV - minV
rangeS = maxS - minS

scaledTrain = []

for i, row in trainData.iterrows():
    scaledTrain.append(((row[0] - minV) / rangeV, (row[1] - minS) / rangeS, row[2]))


def calculate_accuracy(k):
    hit = 0.0
    miss = 0.0
    TP = 0
    TN = 0
    FP = 0
    FN = 0
    for i in scaledTrain:
        distance = []
        judgment = 0

        # get distance
        for j in scaledTrain:
            if i != j:
                distance.append((math.sqrt(numpy.power((i[0] - j[0]), 2) + numpy.power((i[1] - j[1]), 2)), j[2]))
        distance.sort()
        # k th nearest
        for nearest in range(0, k):
            judgment += (distance[nearest])[1]
        # record result
        if judgment > k / 2 and i[2] == 1:
            hit += 1
            TP += 1
        elif judgment <= k / 2 and i[2] == 0:
            hit += 1
            TN += 1
        elif judgment > k / 2 and i[2] == 0:
            miss += 1
            FP += 1
        elif judgment <= k / 2 and i[2] == 1:
            miss += 1
            FN += 1

    print "k = %d, accuracy = %.3f%%" % (k, hit / len(scaledTrain) * 100)
    print "TP %4d TN %4d      SUM %4d" % (TP, TN, TP + TN)
    print "FP %4d FN %4d      SUM %4d" % (FP, FN, FP + FN)
    print


calculate_accuracy(3)
calculate_accuracy(9)
calculate_accuracy(99)

# training
# using k = 3
print ("using k = 3 for testing")

testData = pandas.read_csv('banknote_test.csv', delimiter=',', header=None)

variance = []
skewness = []

# scaling

for i, row in testData.iterrows():
    variance.append(row[0])
    skewness.append(row[1])

scaledTest = []

for i, row in testData.iterrows():
    scaledTest.append(((row[0] - minV) / rangeV, (row[1] - minS) / rangeS, row[2]))

TP = 0
FP = 0
TN = 0
FN = 0

for i in scaledTest:
    distance = []
    judgment = 0

    # get distance
    for j in scaledTrain:
        distance.append((math.sqrt(numpy.power((i[0] - j[0]), 2) + numpy.power((i[1] - j[1]), 2)), j[2]))
    distance.sort()
    # k th nearest
    for nearest in range(0, 3):
        judgment += (distance[nearest])[1]
    # record result
    if judgment > 3 / 2 and i[2] == 1:
        TP += 1
    elif judgment <= 3 / 2 and i[2] == 0:
        TN += 1
    elif judgment > 3 / 2 and i[2] == 0:
        FP += 1
    elif judgment <= 3 / 2 and i[2] == 1:
        FN += 1
print "accuracy: %.3f%%" % (float(TP + TN)/len(scaledTest)*100)
print "TP %4d TN %4d      SUM %4d" % (TP, TN, TP + TN)
print "FP %4d FN %4d      SUM %4d" % (FP, FN, FP + FN)
