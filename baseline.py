import sys
import collections
import re

diseaseMap = {'cancer' : ['cough', 'runny nose', 'heart pain'], 'heart attack' : ['chest pain', 'shortness of breath']}

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
    decision = raw_input("Say yes if you want to, or press another key if you want to quit: ")
    decision.strip(' ')
    match = re.findall('^[Yy][Ee][Ss]', decision)
    print(" ")
    if len(match) > 0:
        return False
    print("See you soon!")
    print(" ")
    return True
    #return True

def baseline(user_input):
    disCounts = collections.defaultdict(int)
    for disease in diseaseMap:
        listOfSymptoms = diseaseMap[disease]
        listOfSymptoms = [x.lower() for x in listOfSymptoms]
        for symptom in user_input:
            if symptom.lower() in listOfSymptoms:
                disCounts[disease] += 1
    if len(disCounts) > 0:
        prediction = max(disCounts)
    else:
        prediction = 'cancer'


    ret = "It sounds like you have " + prediction
    return ret

sympt = ""
intro()
while(True):
    sympt = raw_input("What are your symptoms? ")
    sympt = sympt.split(',')
    sympt = [x.strip(' ') for x in sympt]
    print(" ")
    print(baseline(sympt))
    if wantToQuit():
        break