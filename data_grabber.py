import sys
import collections
import re
import urllib.request
import os

diseases = ['Anthrax', 'Chickenpox', 'Cholera', 'Schistosomiasis',
			'Myocardial Infarction', 'Scabies', 'Influenza', 'Dengue Fever',
			'Mumps virus', 'Rabies', 'Zygomycosis', 'Zika virus'
			'Tuberculosis', 'Syphilis', 'West Nile Fever', 'Sepsis',
			'Rotavirus', 'Q fever', 'Paragonimiasis', 'Measles', 'Kuru',
			'Human metapneumovirus', 'Hand, foot and mouth disease',
			'Gonorrhea']

rawParses = {}

def getText():
    diseasesToCheck = ['_'.join(st.split(' ')) for st in diseases]
    for dis in diseasesToCheck:
        url = "https://en.wikipedia.org/w/api.php?format=json&action=query&prop=extracts&exlimit=max&explaintext&titles=" + dis + "&redirects="
        contents = urllib.request.urlopen(url).read()
        rawParses[' '.join(dis.split('_'))] = str(contents)

getText()

for disease in rawParses:
	filepath = os.path.join('Disease_Data/', disease + ".txt")
	f= open(filepath,"w+")
	f.write(rawParses[disease])
