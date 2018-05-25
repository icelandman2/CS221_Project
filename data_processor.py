import re
import os

path = 'Disease_Data/'

symptomSents = []

for filename in os.listdir(path):
	f = open(path + filename)
	text = "".join(f.read())
	text = text.strip().split('.')
	sents = [re.sub('[^A-Za-z]+', ' ', line) for line in text]

	for s in sents:
		if re.search(r'symptoms', s) != None:
			symptomSents.append(s)

print(symptomSents)
print(len(symptomSents))