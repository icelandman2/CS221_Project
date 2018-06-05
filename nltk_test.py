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
import pprint

path = 'Disease_Data/'
text = ""

train_diseases = {}
with open('train.pickle', 'rb') as handle:
    train_diseases = pickle.load(handle)

rels = ['symptoms include ', 'signs include']

for disease in train_diseases.keys():
	with open(path + disease.replace(' ', '_') + ".txt", encoding='utf-8', errors='replace') as f:
		text = f.read().replace('\\n', ' ').lower()
		text = re.sub('[^A-Za-z.,]+', ' ', text)
		sentences = nltk.sent_tokenize(text)
		'''
		grammar = r"""
				  NP:
				    {<.*>+}          # Chunk everything
				    }<VBD|IN>+{      # Chink sequences of VBD and IN
				  """
		cp = nltk.RegexpParser(grammar)
		
		temp = []
		for rel in rels:
			for sent in sentences:
				if rel in sent:
					if sent not in temp:
						temp.append(sent)

		sentences = [nltk.word_tokenize(sent) for sent in temp]
		sentences = [nltk.pos_tag(sent) for sent in sentences]
		sentences = [cp.parse(sent) for sent in sentences]
		'''
		print(sentences)