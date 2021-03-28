
import sys

text = open(sys.argv[1], "r") 

d = dict() 

words_per_clip = 0
clips = 0

for line in text: 
	line = line.strip() 
	line = line.lower() 
	words = line.split(" ")
	words_per_clip += len(words)
	clips += 1 
	for word in words: 
		if word in d: 
			d[word] = d[word] + 1
		else: 
			d[word] = 1

voc=0
all_words=0
for key in list(d.keys()): 
	print(key, ":", d[key]) 
	voc += 1
	all_words += d[key]

print("Vocab: ", voc)
print("Total Words :", all_words)
print("Average words per clip: ", words_per_clip/clips)