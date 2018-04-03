#!/Library/Frameworks/Python.framework/Versions/3.6/bin/python3.6

import re
# re.search(pattern (str and no forward slashes), subject, options) <- options = re.I (insensitive) or re.S(dot all) or re.M(multiline)
# if re.search ---:
#   do stuff

scrabble, scrabble3, scrabble4, prefix3, prefix4 = set(), set(), set(), set(), set()
words = [line.replace("\n", "") for line in open("wordss.txt")]
# scrabble = {w for w in words if re.search(r"^(?=.*[aeiouy]|cwm|cruth)[a-z]+$", w)}
for w in words:
    if re.search("^\w*[aeiouy]\w*$", w):
        if re.search("^[a-z]*$", w):
            scrabble.add(w)
            if re.search("^[a-z]{3,}$", w):
                scrabble3.add(w)
                prefix3.add(w[:3])
            if re.search("^[a-z]{4,}$", w):
                scrabble4.add(w)
                prefix4.add(w[:4])
print("Number of Scrabble Words: {}".format(len(scrabble)))
print("Number of Scrabble Words (>=3): {}".format(len(scrabble3)))
print("Number of Scrabble Words (>=4): {}".format(len(scrabble4)))
print("Number of distinct {}-letter prefixes: {}".format(3, len(prefix3)))
print("Number of distinct {}-letter prefixes: {}".format(4, len(prefix4)))