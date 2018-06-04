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

path = 'Disease_Data/'

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
with open('obo.pickle', 'rb') as handle:
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
				symptsOfMapped[diseaseName] = symptsForMap

	print(symptsOfMapped)
	with open('./diseaseMaps/handbuilt.pickle', 'wb') as handle:
		pickle.dump(symptsOfMapped, handle, protocol=pickle.HIGHEST_PROTOCOL)


#baseline()
#handbuilt()
