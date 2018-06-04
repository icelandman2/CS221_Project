import sys
import collections
import re
import urllib.request
import os
import difflib

'''
Sentences pulled from the disease's wikipedia page that contain the word 'symptom'
'''

schistosomiasis = "Symptoms include abdominal pain, diarrhea, bloody stool, or blood in the urine.".split()
myocardial_infarction = " Other symptoms may include shortness of breath, nausea, feeling faint, a cold sweat, or feeling tired.[1] About 30% of people have atypical symptoms.".split()
scabies = "The most common symptoms are severe itchiness and a pimple-like rash".split()
influenza = "The most common symptoms include: a high fever, runny nose, sore throat, muscle pains, headache, coughing, and feeling tired".split()
dengue_fever = "Symptoms typically begin three to fourteen days after infection.".split()


diseaseMap = {'Schistosomiasis' : ['rash', 'itching', 'fever', 'aching', 'chills', 'cough', 'diarrhea', 'gland enlargement'],
              'Myocardial Infarction' : ['tightness', 'pressure', 'squeezing', 'chest pain', 'shortness of breath', 'radiating pain', 'sweating', 'nausea', 'vomiting', 'fainting'],
              'Scabies' : ['itching', 'rash', 'crusting'],
              'Influenza' : ['fever', 'chills', 'cough', 'nasal congestion', 'runny nose', 'sneezing'],
              'Dengue Fever' : ['fever', 'headache', 'vomiting', 'joint pain', 'rash']}


symptomMap = {'Schistosomiasis' : schistosomiasis,
              'Myocardial Infarction' : myocardial_infarction,
              'Scabies' : scabies,
              'Influenza' : influenza,
              'Dengue Fever' : dengue_fever}

rels = ['symptoms include (.*?)\.', 'symptoms are (.*?)\.', 'signs include (.*?)\.']

symptsOfMapped = {}

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

def pull_relations():
    for filename in os.listdir('Disease_Data/'):
        #print(filename)
        diseaseName = " ".join(filename[:-4].split("_"))
        filepath = "Disease_Data/" + filename
        f = open(filepath, "r")
        payload = f.readlines()

        for rel in rels:
            found = re.findall(rel, str(payload))
            if len(found)>0:
                rawSympts = found[0]
                rawSympts = re.sub(' and ', ',', rawSympts)
                symptsForMap = []
                for s in rawSympts.split(','):
                    s = s.strip()
                    s = re.sub('[^a-zA-Z\s]', '', s)
                    if len(s) > 1:
                        symptsForMap.append(s)

                if len(symptsForMap)>0:
                    symptsOfMapped[diseaseName] = symptsForMap

    print(symptsOfMapped)
        #print(payload)

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
    #return True

def hand_built(user_input):
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

def baseline(user_input):
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
pull_relations()
while(True):
    sympt = input("What are your symptoms? ")
    sympt = sympt.split(',')
    sympt = [x.strip(' ') for x in sympt]
    print("Here is the baseline prediction:")
    info_from_prediction(baseline(sympt))
    print("Here is the hand-built prediction, without TF-IDF:")
    info_from_prediction(hand_built(sympt))
    if wantToQuit():
        break