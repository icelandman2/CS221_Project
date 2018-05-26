import sys
import collections
import re
import urllib.request
import os
import json
import requests

diseases = ['anthrax', 'chickenpox', 'cholera', 'schistosomiasis',
			'myocardial infarction', 'scabies', 'influenza', 'dengue fever',
			'mumps virus', 'rabies', 'zygomycosis', 'zika virus'
			'tuberculosis', 'syphilis', 'west nile fever', 'sepsis',
			'rotavirus', 'Q fever', 'paragonimiasis', 'measles', 'kuru',
			'human metapneumovirus', 'hand, foot and mouth disease',
			'gonorrhea', 'boutonneuse fever', 'brucellosis', 'campylobacteriosis',
			'cat scratch disease', 'cervicitis', 'chancroid', 'chlamydia',
			'lymphogranuloma venereum', 'clostridial infection', 'dysentery',
			'shigellosis', 'epididymitis', 'glanders', 'leprosy', 'leptospirosis',
			'listeriosis', 'lyme disease', 'in Nombre virus', 'heartland virus',
			'Cryptococcosis']

def getText():
	diseasesToCheck = ['_'.join(st.split(' ')) for st in diseases]
	for dis in diseasesToCheck:
		url = "https://en.wikipedia.org/w/api.php?format=json&action=query&prop=extracts&exlimit=max&explaintext&titles=" + dis + "&redirects=1"

		content = requests.get(url)
		data = content.json()
		filepath = os.path.join('Disease_Data/', dis + ".txt")
		f= open(filepath,"w+")
		json.dump(data, f)

getText()