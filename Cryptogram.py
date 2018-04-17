#!/Library/Frameworks/Python.framework/Versions/3.6/bin/python3.6

import sys
import re
from collections import OrderedDict
import operator

finalMatches = {c: [] for c in "ABCDEFGHIJKLMNOPQRSTUVWXYZ"}

class TrieNode(object):
    def __init__(self, data):
        self.data = data
        self.children = set()
        self.isLeaf = False

    def add_child(self, obj):
        self.children.add(obj)

def main():
    s = sys.argv[1:]
    matches = dict()
    dictionary = [line.rstrip() for line in open("scrabble.txt")]
    root = createTrie(dictionary)
    crypto = ["" for i in range(len(s))]
    for i in range(len(s)):
        for chi in range(len(s[i])):
            if s[i][chi] not in "./?,!;'\"":
                crypto[i] += s[i][chi]
    print("Crypto:", crypto)
    freqCrypto = countFreq(crypto)
    print("FreqCrypto: {}".format(freqCrypto))
    freqLetters = "ETAOINSHRDLCUMWFGYPBVKJXQZ"
    matches = alignFreqLetters(matches, freqCrypto, freqLetters)
    print("MatchesAlign: {}".format(matches))
    sub = makeSub(crypto, matches)
    print("MakeSub: {}".format(sub))
    print(checkIsWord(root, sub, crypto))
    print(finalMatches)
    # pairfreq = {"ss", "ee", "tt", "ff", "ll", "mm", "oo"}
    # twofreq = {"of", "to", "in", "it", "is", "be", "as", "at", "so", "we", "he", "by", "or", "on", "do", "if", "me", "my", "up", "an", "go", "no", "us", "am"}
    # threefreq = {"the", "and", "for", "are", "but", "not", "you", "all", "any", "can", "had", "her", "was", "one", "our", "out", "day", "get", "has", "him", "his", "how", "man", "new", "now", "old", "see", "two", "way", "who", "boy", "did", "its", "let", "put", "say", "she", "too", "use"}
    # fourfreq = {"that", "with", "have", "this", "will", "your", "from", "they", "know", "want", "been", "good", "much", "some", "time"}
    # freqCrypto = {i: crypto.upper().count(i) for i in "ABCDEFGHIJKLMNOPQRSTUVWXYZ"}
    # print("cryptofreq: {}".format(freqCrypto))
    # print("orderfreq: {}".format(orderfreq(freqCrypto)))

def countFreq(crypto):
    total = len([1 for i in crypto for ch in i])
    newDic = {c: 0 for c in "ABCDEFGHIJKLMNOPQRSTUVWXYZ"}
    for c in "ABCDEFGHIJKLMNOPQRSTUVWXYZ":
        for word in crypto:
            newDic[c] += word.count(c)
        newDic[c] = newDic[c]/total
    dic = sorted(newDic.items(), key=operator.itemgetter(1))[::-1]
    return dic

def alignFreqLetters(match, freqC, freqL):
    for i in range(len(freqC)):
        match[freqC[i][0]] = freqL[i]
    return match

def makeSub(s, match):
    newS = ["" for i in range(len(s))]
    for word in range(len(s)):
        for i in range(len(s[word])):
            newS[word] += match[s[word][i]]
    return newS

def checkIsWord(root, cryptoList, originalList):
    global finalMatches
    all = True
    for wordi in range(len(cryptoList)):
        if searchWord(root, cryptoList[wordi], 0):
            for i in range(len(originalList[wordi])):
                finalMatches[originalList[wordi][i]].append(cryptoList[wordi][i])
        else:
            all = False
    return all

def searchWord(node, word, depth):
    # print(node.data)
    # print(word)
    # print(depth)
    # print([k.data for k in node.children])
    if depth == len(word):
        if node.isLeaf:
            return True
    else:
        for k in node.children:
            if k.data == word[depth]:
                return searchWord(k, word, depth + 1)
    return False

def createTrie(dic):
    root = TrieNode(None)
    for word in dic:
        app = True
        for piece in word:
            if piece not in "ABCDEFGHIJKLMNOPQRSTUVWXYZ": app = False
        if app == True:
            node = root
            chars = node.children
            for i in range(len(word)):
                c = word[i]
                if c in {k.data for k in chars}:
                    for ch in chars:
                        if ch.data == c: t = ch
                else:
                    t = TrieNode(word[i])
                    node.add_child(t)
                node = t
                chars = t.children
                if i == len(word) - 1:
                    t.isLeaf = True
    return root

if __name__ == "__main__":
    main()