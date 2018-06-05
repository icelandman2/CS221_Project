import re
import os
import json
import pprint
import collections
import numpy as np
import os
import pandas as pd
import vsm
import pickle
import nltk
from nltk.parse.generate import generate, demo_grammar
from nltk import CFG, Production, Nonterminal

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
	sympts = []
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
				symptsOfMapped[diseaseName] = symptsForMap
				sympts += symptsForMap
	sympts = set(sympts)
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
	print(sympts)
	with open('./diseaseMaps/seeds.txt', 'w') as handle:
		for s in sympts:
			handle.write(s + "\n")

def loadPayloads(name):
	payloads = {}
	train = {}
	with open(name + '.pickle', 'rb') as handle:
		train = pickle.load(handle)

	for d in train.keys():
		d = d.replace(' ', '_')
		f = open(path + d + '.txt', "r", errors='replace')
		payload = f.read()
		payload = re.sub(' and ', ',', payload)
		payload = re.sub(' or ', ',', payload)
		payload = payload.replace('\\n', ',')
		payload = re.sub('[^a-zA-Z.]', ' ', payload)
		payloads[d] = payload
	return payloads

def bootstrap():
	sympts = []
	rels = []
	grammar_sympts = []
	payloads = loadPayloads('train')

	with open('./diseaseMaps/seeds.txt', 'r') as f:
		sympts = f.readlines()
		sympts = [s.strip() for s in sympts]
		grammar_sympts = ["'"+s.strip()+"'" for s in sympts]

	train = {}
	with open('train.pickle', 'rb') as handle:
		train = pickle.load(handle)
	keys = [k.replace(' ', '_') for k in train.keys()]

	symptPatterns = set()
	for d in keys:
		payload = payloads[d]
		sents = payload.split('.')

		for sent in sents:
			inSent = False
			sent = sent.lower()
			for symp in sympts:
				if symp in sent:
					#sent = sent.replace(symp, ' '+ "('SYMP')"+' ')
					sent = sent.replace(symp, ' '+ " (.*) "+' ')
					inSent = True
			sent = sent.split()
			if inSent:
				for i in range(len(sent)-1):
					#if sent[i] == "'SYMP'":
					if sent[i] == "(.*)":
						#toAdd = "'"+" ".join(sent[max(i-3,0):min(i+3, len(sent))])+"'"
						toAdd = " ".join(sent[max(i-3,0):min(i+3, len(sent))])
						symptPatterns.add(toAdd)

	#grammar_sympts = "|".join(grammar_sympts)
	patternScores = collections.defaultdict(int)
	for pattern in symptPatterns:
		for d in keys:
			if patternScores[pattern] > 3: break
			payload = payloads[d]
			found = re.search(pattern, str(payload))
			if found != None:
				patternScores[pattern] += 1
	print(patternScores)
	'''
	for pattern in symptPatterns:
		phrases = []
		pattern = pattern.replace("''", "'")
		words = pattern.split()
		words[0] = words[0].replace("'SYMP", "SYMP")
		words[-1] = words[-1].replace("SYMP'", "SYMP")
		pattern = " ".join(words)
		'''
	'''
		g = CFG.fromstring("""
	 		S -> """ + pattern + """
	 		SYMP -> """ + grammar_sympts)
		for sentence in generate(g, n=100000):
		     phrases.append(''.join(sentence))
		for p in phrases:
			for d in keys:
				payload = payloads[d]
				if p in payload:
					patternScores[pattern] += 1
	print(patternScores)
	'''

def test():
	patterns = "'extract trench 'SYMP' 'SYMP' also'|'confused 'SYMP' also'"
	grammar_sympts = "'hello'|'goodbye'"
	'''
	g = CFG.fromstring("""
	 S -> """ + patterns + """
	 SYMP -> """ + grammar_sympts +"""
	 """)
	'''
	g = CFG.fromstring("""
	 S -> """ + patterns + """
	 SYMP -> """+grammar_sympts+"""
	 """)
	print (g)
	for sentence in generate(g, n=10):
		print(' '.join(sentence))


#baseline()
#handbuilt()
#makeSeeds()
bootstrap()
#test()