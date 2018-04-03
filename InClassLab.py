#!/Library/Frameworks/Python.framework/Versions/3.6/bin/python3.6

# import re
# re.search(pattern (str and no forward slashes), subject, options) <- options = re.I (insensitive) or re.S(dot all) or re.M(multiline)
# if re.search ---:
#   do stuff

def findPref(s, length):
    p = set()
    for w in s:
        if len(w) >= length:
            p.add(w[:length])
    return p

words = [line.replace("\n", "") for line in open("wordss.txt")]
scrabble, scrabble3, scrabble4, prefix3, prefix4 = set(), set(), set(), set(), set()
yus, vowel = True, False
for w in words:
    if len(w) > 0:
        for c in w:
            if c not in "abcdefghijklmnopqrstuvwxyz":
                yus = False
                break
        for v in "aeiouy":
            if v in w:
                vowel = True
                break
        if yus == True and vowel == True:
            if len(w) >= 3: scrabble3.add(w)
            if len(w) >= 4: scrabble4.add(w)
            scrabble.add(w)
        yus, vowel = True, False
print("Number of Scrabble Words: {}".format(len(scrabble)))
print("Number of Scrabble Words (>=3): {}".format(len(scrabble3)))
print("Number of Scrabble Words (>=4): {}".format(len(scrabble4)))
print("Number of distinct {}-letter prefixes: {}".format(3, len(findPref(scrabble3, 3))))
print("Number of distinct {}-letter prefixes: {}".format(4, len(findPref(scrabble4, 4))))
