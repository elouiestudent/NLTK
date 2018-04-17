#!/Library/Frameworks/Python.framework/Versions/3.6/bin/python3.6

import sys
import re
from collections import OrderedDict
import operator

matches = {c: set() for c in "ABCDEFGHIJKLMNOPQRSTUVWXYZ"}

# class TrieNode(object):
#     def __init__(self, data):
#         self.data = data
#         self.children = set()
#         self.isLeaf = False
#
#     def add_child(self, obj):
#         self.children.add(obj)

def main():
    global matches
    s = sys.argv[1:]
    dictionary = [line.rstrip() for line in open("scrabble.txt")]
    # root = createTrie(dictionary)
    crypto = ["" for i in range(len(s))]
    for i in range(len(s)):
        for chi in range(len(s[i])):
            if s[i][chi] not in "./?,!;'\"":
                crypto[i] += s[i][chi]
    cryptoMatching = {crypto[i]: wordPattern(crypto[i]) for i in range(len(crypto))}
    # print(cryptoMatching.values())
    patToDict = dictLengths({k: set() for k in cryptoMatching.values()})
    # print("CryptoMatching: {}".format(cryptoMatching))
    # print("PatternsToDictionary: {}".format(patToDict))
    poss = list()
    for k in cryptoMatching:
        poss.append(addPoss(k, cryptoMatching[k], patToDict))
        # print(poss)
    # print("Mappings: {}".format(poss))
    intersections = {k: {} for k in "ABCDEFGHIJKLMNOPQRSTUVWXYZ"}
    for d in poss:
        intersections = combine(intersections, d)
    # print("Intersections: {}".format(intersections))
    fmatches = findMatches(intersections)
    # print("FindMatches: {}".format(fmatches))
    # print("Matches: {}".format(matches))
    print("MainSolver:", " ".join(mainSolver(intersections, crypto, cryptoMatching, patToDict, "ETAOINSHRDLCUMWFGYPBVKJXQZ", countFreq(crypto))))

def countFreq(crypto):
    total = len([1 for i in crypto for ch in i])
    newDic = {c: 0 for c in "ABCDEFGHIJKLMNOPQRSTUVWXYZ"}
    for c in "ABCDEFGHIJKLMNOPQRSTUVWXYZ":
        for word in crypto:
            newDic[c] += word.count(c)
        newDic[c] = newDic[c]/total
    dic = sorted(newDic.items(), key=operator.itemgetter(1))[::-1]
    return "".join([k[0] for k in dic])

def mainSolver(intersections, crypto, cryptoMatching, patToDict, commonFreq, cryptoFreq):
    tester = ["" for k in crypto]
    for i in range(len(crypto)):
        for ch in crypto[i]:
            tester[i] += "_"
    for k in matches:
        if len(matches[k]) > 0:
            tester = testerReplacer(tester, crypto, k, list(matches[k])[0])
            commonFreq.replace(list(matches[k])[0], "")
            cryptoFreq.replace(k, "")
    newCryptoFreq = ""
    for ch in cryptoFreq:
        if ch in "".join(crypto):
            newCryptoFreq += ch
    # print("tester:", tester)
    longShortSort = sorted([(len(crypto[i]), i) for i in range(len(crypto))])[::-1]
    # print(longShortSort)
    longShortSort = [i[1] for i in longShortSort]
    # print(longShortSort)
    newMatch = dict()
    for k in matches:
        if len(matches[k]) > 0:
            newMatch[k] = matches[k]
    return recurseFrequencies(tester, longShortSort, 0, crypto, patToDict, cryptoMatching, intersections, newMatch)

def recurseFrequencies(test, longToShort, indexLS, crypto, patToDict, cryptoMatching, intersections, cToT):
    print("test:", " ".join(test))
    if indexLS == len(longToShort):
        return test
    bigRegex = makeRegex(test[longToShort[indexLS]])
    for posWord in patToDict[cryptoMatching[crypto[longToShort[indexLS]]]]:
        # print("posWord:", posWord)
        # print("bigRegex:", bigRegex)
        # print("cToT:", cToT)
        if re.search(bigRegex, posWord):
            newTest = test
            newTest[longToShort[indexLS]] = posWord
            newCToT = dict(cToT)
            reoccur = False
            for i in range(len(crypto[longToShort[indexLS]])):
                # print("cryptochar:", crypto[longToShort[indexLS]][i])
                # print("posWordchar:", posWord[i])
                if (crypto[longToShort[indexLS]][i] in cToT and cToT[crypto[longToShort[indexLS]][i]] != posWord[i]) or (posWord[i] in list(cToT.values()) and notconnected(crypto[longToShort[indexLS]][i], posWord[i], cToT)):
                    reoccur = True
                    break
                newCToT[crypto[longToShort[indexLS]][i]] = posWord[i]
                newTest = testerReplacer(newTest, crypto, crypto[longToShort[indexLS]][i], posWord[i])
            if not reoccur:
                # print("newTest:", newTest)
                wordsExist = True
                for i in range(len(newTest)):
                    aWordExists = False
                    for aPos in patToDict[cryptoMatching[crypto[i]]]:
                        if re.search(makeRegex(newTest[i]), aPos):
                            aWordExists = True
                            break
                    if not aWordExists:
                        wordsExist = False
                        break
                if wordsExist:
                    recur = recurseFrequencies(newTest, longToShort, indexLS + 1, crypto, patToDict, cryptoMatching, intersections, newCToT)
                    if recur:
                        return recur
    return ""

def makeRegex(teststr):
    return teststr.replace("_", "\w")

def notconnected(key, val, dic):
    for k in dic:
        if dic[k] == val and key != k:
            return True
    return False

def testerReplacer(tester, crypto, findChar, repChar):
    newT = ["" for k in crypto]
    for i in range(len(crypto)):
        for ic in range(len(crypto[i])):
            if crypto[i][ic] == findChar:
                newT[i] += repChar
            else:
                newT[i] += tester[i][ic]
    return newT

def createNumberPatternsDict():
    return {line.rstrip(): wordPattern(line.rstrip()) for line in open("scrabble.txt")}

def dictLengths(cryptoPatterns):
    for line in open("scrabble.txt"):
        pattern = wordPattern(line.rstrip())
        if pattern in cryptoPatterns:
            cryptoPatterns[pattern].add(line.rstrip())
    return cryptoPatterns

def wordPattern(word):
    num = 0
    letterNums = {}
    pattern = []
    for ch in word:
        if ch not in letterNums:
            letterNums[ch] = str(num)
            num += 1
        pattern.append(letterNums[ch])
    return ".".join(pattern)

def addPoss(word, pattern, patToDict):
    match = {c: set() for c in "ABCDEFGHIJKLMNOPQRSTUVWXYZ"}
    possWords = patToDict[pattern]
    # if pattern == "0.1":
        # print("TSOPOSWORDS:", possWords)
    for i in range(len(word)):
        for wp in possWords:
            if word[i] != wp[i]:
                match[word[i]].add(wp[i])
    return match

def combine(dict1, dict2):
    newDict = dict()
    for k in dict1:
        if len(dict1[k]) > 0 and len(dict2[k]) > 0:
            newDict[k] = dict1[k] & dict2[k]
        elif len(dict1[k]) == 0:
            newDict[k] = dict2[k]
        else:
            newDict[k] = dict1[k]
    return newDict

def findMatches(intersects):
    global matches
    loop = True
    while loop:
        loop = False
        letters = set()
        for ch in intersects:
            if len(intersects[ch]) == 1:
                matches[ch] = intersects[ch].pop()
                intersects[ch].add(matches[ch])
                letters.add(matches[ch])
        for ch in intersects:
            for l in letters:
                if len(intersects[ch]) != 1 and l in intersects[ch]:
                    intersects[ch].remove(l)
                    if len(intersects[ch]) == 1:
                        loop = True
    return intersects

if __name__ == "__main__":
    main()