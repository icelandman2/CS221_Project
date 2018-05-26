'''
		dis = filename[:-4]
		disDict = collections.defaultdict(int)
		#for word in text.split():
		for line in disSymp:
			for word in line.split():
				if word in commonWords: continue
				words.add(word)
				disDict[word] += 1
		diseaseDicts[dis] = disDict
		
mat = []
for word in words:
	if word in commonWords: continue
	mat.append([diseaseDicts[d][word] for d in diseaseDicts.keys()])



words_matrix = pd.DataFrame(mat, index=list(words), columns=diseaseDicts.keys())
words_matrix = words_matrix.apply(vsm.length_norm, axis=1)

#print(vsm.neighbors('symptoms', words_matrix, distfunc=vsm.cosine))
#print(diseaseDicts)


symptomCounts = collections.defaultdict(int)

for line in symptomSents:
	words = line.split()
	for i in range(1,len(words)):
		symptomCounts[(words[i-1], words[i])] += 1
'''
#print(symptomCounts)