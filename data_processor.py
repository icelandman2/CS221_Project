import re
import os
import json
import pprint

path = 'Disease_Data/'

symptomSents = []

for filename in os.listdir(path):
	with open(path + filename, encoding='utf-8', errors='replace') as f:
		text = f.read()
		text = text.strip().split('.')
		sents = [re.sub('[^A-Za-z]+', ' ', line) for line in text]

		for s in sents:
			if re.search(r'symptoms', s) != None:
				symptomSents.append(s)

print(symptomSents)
print(len(symptomSents))