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
        print(poss)
    # print("Mappings: {}".format(poss))
    intersections = {k: {} for k in "ABCDEFGHIJKLMNOPQRSTUVWXYZ"}
    for d in poss:
        intersections = combine(intersections, d)
    # print("Intersections: {}".format(intersections))
    fmatches = findMatches(intersections)
    # print("FindMatches: {}".format(fmatches))
    # print("Matches: {}".format(matches))
    print("MainSolver:", mainSolver(intersections, crypto, cryptoMatching, patToDict, "ETAOINSHRDLCUMWFGYPBVKJXQZ", countFreq(crypto)))

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
    print("tester:", tester)
    return recurseFrequencies(tester, crypto, commonFreq, newCryptoFreq, patToDict, cryptoMatching, intersections)

def recurseFrequencies(test, crypto, commonFreq, cryptoFreq, patToDict, cryptoMatching, intersections):
    print("recurseFreq<")
    if "_" not in "".join(test):
        return test
    print("cryptoFreqBeg:", cryptoFreq)
    print("commonFreqBeg:", commonFreq)
    for cryptoF in cryptoFreq:
        for commonF in commonFreq:
            print("commonF:", commonF)
            print("cryptoF:", cryptoF)
            print("commonFreq:", commonFreq)
            print("cryptoFreq:", cryptoFreq)
            print("test:", test)
            if commonF in intersections[cryptoF]:
                print("pastcommonF:", commonF)
                print("pastcryptoF:", cryptoF)
                newTest = testerReplacer(test, crypto, cryptoF, commonF)
                print("newTest:", newTest)
                isPos = True
                for i in range(len(newTest)):
                    regex = newTest[i].replace("_", "\w")
                    print("regex:", regex)
                    wordPoss = False
                    print("newTest[i]:", newTest[i], "dictWord:", patToDict[cryptoMatching[crypto[i]]])
                    for dictWord in patToDict[cryptoMatching[crypto[i]]]:
                        if re.search(regex, dictWord):
                            print("foundInPathToDic")
                            wordPoss = True
                            break
                    if not wordPoss:
                        print("notFound")
                        isPos = False
                        break
                if not isPos:
                    print("notIsPosContinue")
                    continue
                else:
                    print("recurseFreqSome>")
                    return recurseFrequencies(newTest, crypto, commonFreq.replace(commonF, ""), cryptoFreq.replace(cryptoF, ""), patToDict, cryptoMatching, intersections)
    print("recurseFreqNone>")
    return ""

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
    if pattern == "0.1":
        print("TSOPOSWORDS:", possWords)
    for i in range(len(word)):
        for wp in possWords:
            if wp[i] != word[i]:
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

# def countFreq(crypto):
#     total = len([1 for i in crypto for ch in i])
#     newDic = {c: 0 for c in "ABCDEFGHIJKLMNOPQRSTUVWXYZ"}
#     for c in "ABCDEFGHIJKLMNOPQRSTUVWXYZ":
#         for word in crypto:
#             newDic[c] += word.count(c)
#         newDic[c] = newDic[c]/total
#     dic = sorted(newDic.items(), key=operator.itemgetter(1))[::-1]
#     return dic
#
# def alignFreqLetters(match, freqC, freqL):
#     for i in range(len(freqC)):
#         match[freqC[i][0]] = freqL[i]
#     return match
#
# def makeSub(s, match):
#     newS = ["" for i in range(len(s))]
#     for word in range(len(s)):
#         for i in range(len(s[word])):
#             newS[word] += match[s[word][i]]
#     return newS
#
# def checkIsWord(root, cryptoList, originalList):
#     global finalMatches
#     all = True
#     for wordi in range(len(cryptoList)):
#         if searchWord(root, cryptoList[wordi], 0):
#             for i in range(len(originalList[wordi])):
#                 finalMatches[originalList[wordi][i]].append(cryptoList[wordi][i])
#         else:
#             all = False
#     return all
#
# def searchWord(node, word, depth):
#     # print(node.data)
#     # print(word)
#     # print(depth)
#     # print([k.data for k in node.children])
#     if depth == len(word):
#         if node.isLeaf:
#             return True
#     else:
#         for k in node.children:
#             if k.data == word[depth]:
#                 return searchWord(k, word, depth + 1)
#     return False
#
# def createTrie(dic):
#     root = TrieNode(None)
#     for word in dic:
#         app = True
#         for piece in word:
#             if piece not in "ABCDEFGHIJKLMNOPQRSTUVWXYZ": app = False
#         if app == True:
#             node = root
#             chars = node.children
#             for i in range(len(word)):
#                 c = word[i]
#                 if c in {k.data for k in chars}:
#                     for ch in chars:
#                         if ch.data == c: t = ch
#                 else:
#                     t = TrieNode(word[i])
#                     node.add_child(t)
#                 node = t
#                 chars = t.children
#                 if i == len(word) - 1:
#                     t.isLeaf = True
#     return root

if __name__ == "__main__":
    main()