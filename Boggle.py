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
        # self.isLeaf = False

def readIn(str):
    b = list()
    row, count = 0, 0
    while count < len(str):
        if str[count] in "123456789":
            b.append(str[count + 1: count + 1 + int(str[count])])
            count = count + 1 + int(str[count])
        else:
            if str[count] == "_": b.append(" ")
            else: b.append(str[count])
            count += 1
    s = int(math.pow(len(b), 0.5))
    # print("b:", b)
    # print("size:", s)
    board = {i:[] for i in range(s)}
    for c in b:
        if len(board[row]) == s: row += 1
        board[row].append(c)
    # print("board:", board)
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
    # print("adjacent:", adjacent)
    return adjacent

def createTrie(dic):
    root = TrieNode(None)
    # count = 0
    for word in dic:
        # if count == 10:
        #     break
        app = True
        for piece in word:
            if piece not in "abcdefghijklmnopqrstuvwxyz":
                app = False
        if app == True:
            node = root
            chars = node.children
            # print("word: {}".format(word))
            for i in range(len(word)):
                # print("chars: {}".format(root.children.keys()))
                # print("chars: {}".format({k.data for k in node.children}))
                c = word[i]
                # print("c: {}".format(c))
                if c in {k.data for k in chars}:
                    # print("inChars")
                    for ch in chars:
                        if ch.data == c:
                            t = ch
                else:
                    # print("notinChars")
                    # print("char:", c, "chars:", {h.data for h in chars})
                    t = TrieNode(word[i])
                    node.add_child(t)
                node = t
                chars = t.children
                if i == len(word) - 1:
                    print("word:", word)
                    t.isLeaf = True
                    print("t.data", t.data)
                    print("t.isLeaf:", t.isLeaf)
            # count += 1
    return root

# def findWords(board, size, row, col, str, adj, visited, dic):
    # w = set()
    # visited[(row, col)] = True
    # str = str + board[row][col]
    # print("str:", str)
    # if str in dic:
    #     if size == 4 and len(str) >= 3:
    #         w.add(str)
    #     elif len(str) >= 4:
    #         w.add(str)
    # for cr, cc in adj[(row, col)]:
    #     if visited[(cr, cc)] == False:
    #         print("w:", w)
    #         w = w.union(findWords(board, size, cr, cc, str, adj, visited, dic))
    # visited[(row, col)] = False
    # return w
    # for word in dic:
    #     mini = 0
    #     if size == 4:
    #         mini = 3
    #     elif size > 4:
    #         mini = 4
    #     if len(word) >= mini:
    #         for k in range(len(word)):
    #             for r in range(size):
    #                 for c in range(size):
    #                     if board[r][c] == word[k]:
    #                         s = board[r][c]
    #                         for i in range(1, len(word)):

# def printout(node):
    # s = set()
    # # print(node.children)
    # for k in node.children:
    #     print(node.children[k].data)
    #     s.add(node.children[k].data)
    # for k in node.children:
        # print("Key: {}, Value: {}".format(k, node.children[k].data))
        # print("Key: {}".format(k))
    # print("Node: {}, Children Chars: {}, Children Values: {}".format(node.data, node.children.keys(), {node.children[k].data for k in node.children}))

def findWords(root, board, adjacent, size):
    words = set()
    length = 0
    if size == 4:
        length = 3
    elif size > 4:
        length = size - 1
    print("length:", length)
    v = {(i, j):False for i, j in adjacent}
    for r, c in adjacent:
        v[r, c] = True
        words = words.union(recurseWords(root, "", r, c, board, adjacent, v, length))
        v[r, c] = False
    return words

def recurseWords(node, str, row, col, board, adjacent, visited, l):
    s = set()
    c = adjacent[row, col]
    print("c:", c)
    print("nodeval:", node.data)
    print("adjacent chars:", [board[k][h] for k, h in adjacent[row, col]])
    for k in node.children:
        # print("row:", row, "col:", col)
        # print("c:", c)
        for i, j in c:
            if k.data == board[i][j] and not visited[(i, j)]:
                print("str added:", str + k.data)
                print("k.isLeaf:", k.isLeaf)
                print("k.data:", k.data)
                print("children:", {n.data for n in node.children})
                if k.isLeaf and len(str + k.data) >= l:
                    s.add(str + k.data)
                print("s:", s)
                visited[(i, j)] = True
                s = s.union(recurseWords(k, str + k.data, i, j, board, adjacent, visited, l))
                visited[(i, j)] = False
            # elif not k.isLeaf:
            #     s = s.union(recurseWords(k, str + k.data, i, j, board, adjacent, l))
    return s

dictionary = [line.rstrip() for line in open("wordss.txt")]
board, size = readIn("mlsteaefnonctcan")
adjacent = createAdjacent(size)
# visited = {(i, j): False for i, j in adjacent}
# words = set()
# for row, col in adjacent:
#     words = words.union(findWords(board, size, row, col, "", adjacent, visited, dictionary))
# print("words:", words)
# print("#:", len(words))
root = createTrie(dictionary)
words = findWords(root, board, adjacent, size)
correctwords = {'nonce', 'steal', 'meals', 'easel', 'none', 'set', 'man', 'net', 'ale', 'team', 'ales', 'canon', 'annals', 'seam', 'tea', 'slant', 'aces', 'enact', 'lean', 'men', 'ease', 'cannot', 'anon', 'conceal', 'coal', 'canes', 'noels', 'ant', 'seamen', 'mast', 'lent', 'coals', 'cancels', 'tone', 'meant', 'can', 'eon', 'cone', 'tonal', 'lea', 'manes', 'canals', 'not', 'manna', 'canal', 'cannon', 'fen', 'lane', 'nest', 'name', 'lanes', 'slam', 'tenon', 'lest', 'anal', 'meanest', 'lance', 'con', 'tones', 'tenant', 'cancel', 'canoe', 'feast', 'cot', 'lancet', 'ton', 'anneal', 'east', 'steam', 'teas', 'cones', 'lame', 'coast', 'fest', 'let', 'neon', 'canoes', 'toast', 'elm', 'sea', 'leas', 'toes', 'enamels', 'lament', 'teal', 'cane', 'sane', 'least', 'aeon', 'teals', 'nets', 'male', 'ones', 'senna', 'else', 'enamel', 'anneals', 'acne', 'amen', 'lam', 'sale', 'mas', 'ace', 'left', 'lancets', 'last', 'ten', 'mean', 'same', 'conceals', 'lease', 'non', 'males', 'concealment', 'one', 'meal', 'lefts', 'lances', 'toe', 'once', 'noes', 'lets', 'leanest', 'seal', 'noel', 'mane', 'act'}
print("Correct Words: {}".format(correctwords))
print("Correct #: {}".format(len(correctwords)))
print("Final Words: {}".format(words))
print("#: {}".format(len(words)))
print("Missing Words: {}".format({k for k in correctwords if k not in words}))
# printout(root)
