#!/Library/Frameworks/Python.framework/Versions/3.6/bin/python3.6

import sys
import math

class TrieNode(object):
    def __init__(self, data):
        self.data = data
        self.children = set()
        self.isLeaf = False

    def add_child(self, obj):
        self.children.add(obj)

def readIn(str):
    b = list()
    row, count = 0, 0
    while count < len(str):
        if str[count] in "123456789":
            b.append(str[count + 1: count + 1 + int(str[count])].lower())
            count = count + 1 + int(str[count])
        else:
            b.append(str[count].lower())
            count += 1
    s = int(math.pow(len(b), 0.5))
    board = {i:[] for i in range(s)}
    for c in b:
        if len(board[row]) == s: row += 1
        board[row].append(c)
    return board, s

def createAdjacent(size):
    adjacent = dict()
    for r in range(size):
        for c in range(size):
            adjacent[(r, c)] = set()
            if r < size - 1: adjacent[(r, c)].add((r + 1, c))
            if r > 0: adjacent[(r, c)].add((r - 1, c))
            if c < size - 1: adjacent[(r, c)].add((r, c + 1))
            if c > 0: adjacent[(r, c)].add((r, c - 1))
            if r < size - 1 and c < size - 1: adjacent[(r, c)].add((r + 1, c + 1))
            if r < size - 1 and c > 0: adjacent[(r, c)].add((r + 1, c - 1))
            if r > 0 and c < size - 1: adjacent[(r, c)].add((r - 1, c + 1))
            if r > 0 and c > 0: adjacent[(r, c)].add((r - 1, c - 1))
    return adjacent

def createTrie(dic):
    root = TrieNode(None)
    for word in dic:
        app = True
        for piece in word:
            if piece not in "abcdefghijklmnopqrstuvwxyz": app = False
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

def findWords(root, board, adjacent, size):
    words = set()
    length = 0
    if size == 4: length = 3
    elif size > 4: length = 4
    v = {(i, j):False for i, j in adjacent}
    for r, c in adjacent:
        v[r, c] = True
        temp = root
        for ch in board[r][c]:
            for j in temp.children:
                if j.data == ch: temp = j
        words = words.union(recurseWords(temp, board[r][c], r, c, board, adjacent, v, length))
        v[r, c] = False
    return words

def recurseWords(node, str, row, col, board, adjacent, visited, l):
    s = set()
    c = adjacent[row, col]
    for k in node.children:
        for i, j in c:
            if not visited[i, j] and board[i][j] != "_":
                if len(board[i][j]) == 1:
                    if k.data == board[i][j]:
                        if k.isLeaf and len(str + k.data) >= l: s.add(str + k.data)
                        visited[(i, j)] = True
                        s = s.union(recurseWords(k, str + k.data, i, j, board, adjacent, visited, l))
                        visited[(i, j)] = False
                else:
                    block = board[i][j]
                    temp = node
                    seg = ""
                    for ch in block:
                        for h in temp.children:
                            if h.data == ch:
                                temp = h
                                seg += ch
                    if seg == board[i][j]:
                        visited[(i, j)] = True
                        s = s.union(recurseWords(temp, str + seg , i, j, board, adjacent, visited, l))
                        visited[(i, j)] = False
    return s

inp = sys.argv[1]
dictionary = [line.rstrip().lower() for line in open("scrabble.txt")]
board, size = readIn(inp)
print("board: \n")
for i in board:
    print(board[i])
adjacent = createAdjacent(size)
root = createTrie(dictionary)
words = findWords(root, board, adjacent, size)
print("Final Words: {}".format(words))
print("#: {}".format(len(words)))