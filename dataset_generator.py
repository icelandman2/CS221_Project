import re
import os
import random
import pickle

def buildFullDataSet():
	diseaseSymptomMap = {}
	terms = []
	with open('doid.obo.txt', errors='replace') as f:
		text = f.read()
		text = text.split("\n[Term]\n")
		for term in text:
			terms.append(term)
	for term in terms:
		name_search = re.findall('name: [^\n]*', term)
		name = ""
		for name in name_search:
			name = name.replace("name: ", "")
		sympt_search = re.findall('has_symptom[^(\n|.|,)]*', term)
		for sympt in sympt_search:
			s = sympt.split()
			s = " ".join(s[1:])
			s = s.replace(" and has_symptom ", "$")
			s = s.replace(" or has_symptom ", "$").strip()
			s = s.split("$")
			diseaseSymptomMap[name.lower()] = s

	with open('./diseaseMaps/full.pickle', 'wb') as handle:
	    pickle.dump(diseaseSymptomMap, handle, protocol=pickle.HIGHEST_PROTOCOL)

def splitData():
	diseases = {}
	with open('full.pickle', 'rb') as handle:
		diseases = pickle.load(handle)

	numTotal = len(diseases)
	numTrain = int(numTotal * .8)
	numTest = numTotal - numTrain
	numVal = int(numTrain * .8)
	numTrain -= numVal

	keys = list(diseases.keys())

	train = {}
	val = {}
	test = {}
	for i in range(numTrain):
		k = random.choice(keys)
		train[k] = diseases[k]
		keys.remove(k)
	for i in range(numVal):
		k = random.choice(keys)
		val[k] = diseases[k]
		keys.remove(k)
	for i in range(numTest):
		k = random.choice(keys)
		test[k] = diseases[k]
		keys.remove(k)
		with open('test.pickle', 'wb') as handle:
			pickle.dump(test, handle, protocol=pickle.HIGHEST_PROTOCOL)
		with open('train.pickle', 'wb') as handle:
			pickle.dump(train, handle, protocol=pickle.HIGHEST_PROTOCOL)
		with open('val.pickle', 'wb') as handle:
			pickle.dump(val, handle, protocol=pickle.HIGHEST_PROTOCOL)

buildFullDataSet()	
#splitData()
    	

