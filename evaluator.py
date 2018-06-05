import sys
import collections
import re
import urllib.request
import os
import difflib
import pickle

def loadMap(file):
	with open('./diseaseMaps/' + file + '.pickle', 'rb') as handle:
   		return pickle.load(handle)

full = loadMap('full')
baseline = loadMap('baseline')
handbuilt = loadMap('handbuilt')

def evaluate_datasets(cmp_dataset, name="baseline"):
    print("Evaluation results for gold parses compared to dataset " + name)
    disToScoreTuple = {}
    avgP = 0
    avgR = 0
    nums = 0
    for disease in cmp_dataset.keys():
        nums = nums+1
        numRelevant = 0
        numRetrieved = len(cmp_dataset[disease])
        totalRecall = len(full[disease])
        precision = 0
        recall = 0
        if numRetrieved > 0:
            for sympt in cmp_dataset[disease]:
                for goldS in full[disease]:

                    if goldS in sympt:
                        numRelevant = numRelevant + 1
                        break

            precision = float(numRelevant) / float(numRetrieved)
            recall = float(numRelevant) / float(totalRecall)

        #print(precision, recall)
        avgP = avgP+precision
        avgR = avgR+recall

    def calc_f1(p, r):
        num = 2 * p * r
        denom = p + r
        return float(num) / float(denom)

    avgP = float(avgP) / float(nums)
    avgR = float(avgR) / float(nums)

    print("Precision: " + str(round(avgP, 4)))
    print("Recall: " + str(round(avgR, 4)))
    print("F1 Score: " + str(round(calc_f1(avgP, avgR), 4)))



evaluate_datasets(baseline)
evaluate_datasets(handbuilt, name="handbuilt")