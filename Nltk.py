#!/Library/Frameworks/Python.framework/Versions/3.6/bin/python3.6

# from nltk.book import *
# from nltk.corpus import words

# text = text4
# text = words.words()
text = [line.split() for line in open("tax.txt")]
# text = [line.split() for line in open("bookreport.txt")]
unique = set()
notunique = list()
for l in text:
    for w in l:
        print(w)
        unique.add(w)
        notunique.append(w)
# unique = set(text)
# notunique = text
print(unique)
print("Number of Words: {}".format(len(notunique)))
print("Number of Unique Words: {}".format(len(unique)))
print("Average Length of Unique Words: {}".format(sum(len(w) for w in unique)/len(unique)))
print("Average Number of Vowels per Unique Word: {}".format(len([c for w in unique for c in w if c in "aeiouy"])/len(unique)))