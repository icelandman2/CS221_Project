import sys
import collections
import re
import urllib.request
import os
import difflib
import pickle
import random

def loadMap(file):
	with open('./diseaseMaps/' + file + '.pickle', 'rb') as handle:
   		return pickle.load(handle)

full = loadMap('full')
baseline = loadMap('baseline')
handbuilt = loadMap('handbuilt')

for i in range(3):
	k = random.choice(list(handbuilt.keys()))
	print('baseline')
	print(k, baseline[k])
	print('handbuilt')
	print(k, handbuilt[k])

def intro():
    print(" ")
    print("Hello! My name is Dr. Gogol! I am an automated search assistant.")
    print("Tell me a bit about your symptoms, and I will tell you if I have a diagnosis.")
    print("Please keep in mind that this is for educational purposes only.")
    print("I am not an actual medical professional.")
    print("I am not intended to diagnose, cure, prevent, or treat any disease.")
    print("Please contact your doctor if you have any medical questions.")
    print("With that in mind, let's go!")
    print(" ")

def wantToQuit():
    print(" ")
    print("Do you want to ask about another condition?")
    decision = input("Say yes if you want to, or press another key if you want to quit: ")
    decision.strip(' ')
    match = re.findall('^[Yy][Ee][Ss]', decision)
    print(" ")
    if len(match) > 0:
        return False
    print("See you soon!")
    print(" ")
    return True

def fuzzy_predict(user_input):
    disCounts = collections.defaultdict(int)
    for disease in symptsOfMapped:
        listOfSymptoms = symptsOfMapped[disease]
        listOfSymptoms = [x.lower() for x in listOfSymptoms]
        for symptom in user_input:
            for goldS in listOfSymptoms:
                matchlib = difflib.SequenceMatcher(None, symptom.lower(), goldS.lower())
                isMatch = matchlib.find_longest_match(0,len(symptom),0,len(goldS))
                if isMatch is not None:
                    #print(isMatch.size)
                    if float(isMatch.size) >= .75*float(len(symptom)):
                        matchPortion = float(isMatch.size) / float(len(symptom))
                        disCounts[disease] += matchPortion
                        break
                        #TOOD: Alter to get BEST match, rather than first threshold match
    #print(disCounts)
    if len(disCounts) > 0:
        max = 0
        pred = ""
        for dis in disCounts:
            if disCounts[dis] > max:
                max = disCounts[dis]
                pred = dis
        prediction = pred
    else:
        prediction = 'unknown'

    return prediction

def baseline_predict(user_input, diseaseMap):
    disCounts = collections.defaultdict(int)
    for disease in diseaseMap:
        listOfSymptoms = diseaseMap[disease]
        listOfSymptoms = [x.lower() for x in listOfSymptoms]
        for symptom in user_input:
            if symptom.lower() in listOfSymptoms:
                disCounts[disease] += 1
    if len(disCounts) > 0:
        max = 0
        pred = ""
        for dis in disCounts:
            if disCounts[dis]>max:
                max = disCounts[dis]
                pred = dis
        prediction = pred
    else:
        prediction = 'unknown'

    return prediction

def info_from_prediction(prediction):
    if prediction is not 'unknown':
        outVal = "It sounds like you have " + prediction
        '''
        words_of_wisdom = symptomMap[prediction]
        will later print using this info as well
        '''
        print(outVal)
        #words_of_wisdom = symptomMap[prediction]
        #sent = " ".join(words_of_wisdom)
        #print(sent)
    else:
        print("I'm not sure what you have...")

sympt = ""
intro()
#pull_relations()
while(True):
    sympt = input("What are your symptoms? ")
    sympt = sympt.split(',')
    sympt = [x.strip(' ') for x in sympt]
    print("Here is the baseline prediction:")
    info_from_prediction(baseline_predict(sympt, baseline))
    print("Here is the hand-built prediction, without TF-IDF:")
    info_from_prediction(baseline_predict(sympt, handbuilt))
    if wantToQuit():
        break