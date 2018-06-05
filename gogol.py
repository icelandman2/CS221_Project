import sys
import collections
import re
import urllib.request
import os
import difflib
import pickle
import random
import math

def loadMap(file):
	with open('./diseaseMaps/' + file + '.pickle', 'rb') as handle:
   		return pickle.load(handle)

full = loadMap('full')
baseline = loadMap('baseline')
handbuilt = loadMap('handbuilt')


#proof-of-concept of prevalence-mapping (no prepared dataset available)
handMadeIncidence = {"swine influenza" : 5000000, "bronchitis" : 350000000, "pulmonary tuberculosis" : 2300000000,
"genital herpes" : 846000000, "rocky mountain spotted fever": 15000, "gonorrhea" : 49000000, "measles":20000000,
"appendicitis": 11600000, "west nile virus infectious disease":5500, "aids related complex":1800000,  "marburg hemorrhagic fever":550,
"infectious mononucleosis":3150000, "plantar wart":350000000,  "human immunodeficiency virus infectious disease":1800000,
"lyme disease":365000, "toxic shock syndrome":210000, "rubella":500000000,  "celiac disease":51851000, "anthrax disease":2500, "hepatitis a":114000000,
"leprosy":514000, "hepatitis b":356000000, "japanese encephalitis":68000, "chickenpox":4000000, "mumps":550000,
"dengue hemorrhagic fever":20000,  "hepatitis c":143000000,  "zika fever":150000
}

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
            bestL = 0.0
            for goldS in listOfSymptoms:
                matchlib = difflib.SequenceMatcher(None, symptom.lower(), goldS.lower())
                isMatch = matchlib.find_longest_match(0,len(symptom),0,len(goldS))
                if isMatch is not None:
                    #print(isMatch.size)
                    if float(isMatch.size) >= .75*float(len(symptom)):
                        matchPortion = float(isMatch.size) / float(len(symptom))
                        if bestL > matchPortion:
                            bestL = matchPortion
            disCounts[disease] += matchPortion

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

def baseline_predict(user_input, diseaseMap, use_handmade_incidence=False):
    disCounts = collections.defaultdict(int)
    for disease in diseaseMap:
        listOfSymptoms = diseaseMap[disease]
        listOfSymptoms = [x.lower() for x in listOfSymptoms]
        for symptom in user_input:
            if symptom.lower() in listOfSymptoms:
                disCounts[disease] += 1

    if use_handmade_incidence:
        for disease in disCounts:
            if disease in handMadeIncidence:
                disCounts[disease] *= math.log(handMadeIncidence[disease], 10) #multiplied to preserve a priori symptom data better
                
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
    print("Here's the experimental hand-built predictor, with log-likelihood:")
    info_from_prediction(baseline_predict(sympt, handbuilt, use_handmade_incidence=True))
    if wantToQuit():
        break