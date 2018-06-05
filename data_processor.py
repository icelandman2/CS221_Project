import re
import os
import json
import pprint
import collections
import numpy as np
import os
import vsm
import pickle
import nltk

path = './Disease_Data/'

commonWords = 'a,able,about across after,all,almost,also,am,among,an,and,\
			   any,are,as,at,be,because,been,but,by,can,cannot,could,dear,\
			   did,do,does,either,else,ever,every,for,from,get,got,had,has,\
			   have,he,her,hers,him,his,how,however,i,if,in,into,is,it,its,\
			   just,least,let,like,likely,may,me,might,most,must,my,neither,\
			   no,nor,not,of,off,often,on,only,or,other,our,own,rather,said,\
			   say,says,she,should,since,so,some,than,that,the,their,them,\
			   then,there,these,they,this,tis,to,too,twas,us,wants,was,we,\
			   were,what,when,where,which,while,who,whom,why,will,with,would,\
			   yet,you,your, those, such, have, more'


diseases = []
with open('./diseaseMaps/full.pickle', 'rb') as handle:
    diseases = pickle.load(handle).keys()

def baseline():
	diseaseSymptomMap = {}
	for d in diseases:
		disease = d.replace(" ", "_")
		symptoms = set()
		with open(path + disease + ".txt", encoding='utf-8', errors='replace') as f:
			text = f.read().replace('\\n', ' ').lower()
			text = re.sub('[^A-Za-z.]+', ' ', text)
			sents = text.split('.')
			for sent in sents:
				if "symptom" in sent:
					sent = sent.split()
					sent = set(sent)
					symptoms = symptoms.union(sent)
		diseaseSymptomMap[d] = list(symptoms)
	with open('./diseaseMaps/baseline.pickle', 'wb') as handle:
	    pickle.dump(diseaseSymptomMap, handle, protocol=pickle.HIGHEST_PROTOCOL)

def handbuilt():
	symptsOfMapped = {}
	rels = ['symptoms include (.*?)\.', 'symptoms are (.*?)\.', 'signs include (.*?)\.']

	for filename in os.listdir('Disease_Data/'):
	#print(filename)
		diseaseName = " ".join(filename[:-4].split("_"))
		filepath = "Disease_Data/" + filename
		f = open(filepath, "r", errors='replace')
		payload = f.readlines()

		for rel in rels:
			found = re.findall(rel, str(payload))
			rawSympts = ""
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
				symptsOfMapped[diseaseName.lower()] = symptsForMap
	with open('./diseaseMaps/handbuilt.pickle', 'wb') as handle:
		pickle.dump(symptsOfMapped, handle, protocol=pickle.HIGHEST_PROTOCOL)

def makeSeeds():
	sympts = []
	rels = ['(?<=symptoms include)[^(\n|.|,)]*', '(?<=signs include)[^(\n|.|,)]*']

	for filename in os.listdir('Disease_Data/'):
		diseaseName = " ".join(filename[:-4].split("_"))
		filepath = "Disease_Data/" + filename
		f = open(filepath, "r", errors='replace')
		payload = f.readlines()

		for rel in rels:
			found = re.findall(rel, str(payload))
			rawSympts = ""
			if len(found)>0:
				rawSympts = found[0]
				rawSympts = re.sub(' and ', ',', rawSympts)
				rawSympts = re.sub(' or ', ',', rawSympts)
				rawSympts = rawSympts.replace('\\n', ',')
			symptsForMap = []
			for s in rawSympts.split(','):
				s = re.sub('[^a-zA-Z\s]', ' ', s)
				s = s.strip().lower()
				if len(s) > 1:
					symptsForMap.append(s)
				sympts += symptsForMap
	sympts = set(sympts)
	with open('./diseaseMaps/seeds.txt', 'w') as handle:
		for s in sympts:
			handle.write(s + "\n")

def loadPayloads(name):
	payloads = {}
	train = {}
	with open(name + '.pickle', 'rb') as handle:
		train = pickle.load(handle)

	for d in train.keys():
		filename = d.replace(' ', '_')
		f = open(path + filename + '.txt', "r", errors='replace')
		payload = f.read()
		payload = re.sub(' and ', ',', payload)
		payload = re.sub(' or ', ',', payload)
		payload = payload.replace('\\n', ',')
		payload = re.sub('[^a-zA-Z.]', ' ', payload)
		payloads[d] = payload
	return payloads

def bootstrapMatch():
	sympts = []
	symptsOfMapped = {}
	rels = []
	with open('./diseaseMaps/bootstrapRels.txt', 'r') as handle:
		rels = handle.read().split('\n')
	print(rels)
	return
	payloads = loadPayloads('./diseaseMaps/train')
	keys = [k for k in payloads.keys()]

	for k in keys:
		payload = payloads[k]
		for rel in rels:
			found = re.search(rel, payload)
			if found == None: continue
			phrase = found.group()
			excessWords = rel.split('(.){0,20}')
			for excess in excessWords:
				phrase = phrase.replace(excess, ',')
			symptsForMap = []
			for s in phrase.split(','):
				s = s.strip()
				s = re.sub('[^a-zA-Z\s]', '', s)
				if len(s) > 1:
					symptsForMap.append(s)
			if len(symptsForMap)>0:
				symptsOfMapped[k.lower()] = symptsForMap
	print(symptsOfMapped)
	with open('./diseaseMaps/bootstrap.pickle', 'wb') as handle:
		pickle.dump(symptsOfMapped, handle, protocol=pickle.HIGHEST_PROTOCOL)


def bootstrap():
	sympts = []
	rels = []
	grammar_sympts = []
	payloads = loadPayloads('./diseaseMaps/train')

	with open('./diseaseMaps/seeds.txt', 'r') as f:
		sympts = f.readlines()
		sympts = [s.strip() for s in sympts]
		grammar_sympts = ["'"+s.strip()+"'" for s in sympts]

	train = {}
	with open('./diseaseMaps/train.pickle', 'rb') as handle:
		train = pickle.load(handle)
	keys = [k for k in train.keys()]

	symptPatterns = set()
	for d in keys:
		payload = payloads[d]
		sents = payload.split('.')

		for sent in sents:
			inSent = False
			sent = sent.lower()
			for symp in sympts:
				if symp in sent:
					sent = sent.replace(symp, " (.){0,20} ")
					inSent = True
			sent = sent.split()
			if inSent:
				for i in range(len(sent)-1):
					if sent[i] == "(.){0,20}":
						toAdd = " ".join(sent[max(i-3,0):min(i+3, len(sent))])
						symptPatterns.add(toAdd)

	patternScores = collections.defaultdict(int)
	count = 0
	total = len(symptPatterns)
	for pattern in symptPatterns:
		print("Pattern: " + str(count) + "/" + str(total))
		count += 1
		key_count = 0
		for d in keys:
			if patternScores[pattern] > 3: break
			payload = payloads[d]
			found = re.search(pattern, str(payload))
			if found != None:
				patternScores[pattern] += 1
			#print(found)
	for pattern in patternScores.keys():
		if patternScores[pattern] > 0:
			rels.append(pattern)
	with open('./diseaseMaps/bootstrapRels.txt', 'w') as handle:
		for s in rels:
			handle.write(s + "\n")

	


#baseline()
#handbuilt()
#makeSeeds()
#bootstrap()
bootstrapMatch()
