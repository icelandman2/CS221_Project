import re
import os
import pickle


symptomWords = set()
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
	#Possibly include synonyms
	for name in name_search:
		name = name.replace("name: ", "")
	sympt_search = re.findall('has_symptom[^(\n|.|,)]*', term)
	for sympt in sympt_search:
		s = sympt.split()
		s = " ".join(s[1:])
		s = s.replace(" and has_symptom ", "$")
		s = s.replace(" or has_symptom ", "$").strip()
		s = s.split("$")
		diseaseSymptomMap[name] = s

with open('obo.pickle', 'wb') as handle:
    pickle.dump(diseaseSymptomMap, handle, protocol=pickle.HIGHEST_PROTOCOL)

