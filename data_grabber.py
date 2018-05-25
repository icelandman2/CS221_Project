rawParses = {}
import sys
import collections
import re
import urllib.request

diseases = ['Anthrax', 'Chickenpox', 'Cholera', 'Schistosomiasis',
			'Myocardial Infarction', 'Scabies', 'Influenza', 'Dengue Fever',
			'Mumps virus', 'Rabies']

def getText():
    diseasesToCheck = ['_'.join(st.split(' ')) for st in diseases]
    for dis in diseasesToCheck:
        url = "https://en.wikipedia.org/w/api.php?format=json&action=query&prop=extracts&exlimit=max&explaintext&titles=" + dis + "&redirects="
        contents = urllib.request.urlopen(url).read()
        rawParses[' '.join(dis.split('_'))] = contents
    print(len(rawParses))

getText()
print(rawParses)