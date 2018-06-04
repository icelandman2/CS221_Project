import sys
import collections
import re
import urllib.request
import os
import json
import requests
import pickle

diseases = []
with open('obo.pickle', 'rb') as handle:
    diseases = pickle.load(handle).keys()

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