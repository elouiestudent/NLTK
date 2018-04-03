#!/Library/Frameworks/Python.framework/Versions/3.6/bin/python3.6

import sys
import urllib.request
import html2text

def checkFile(filename):
    try:
        f = open(filename, "r")
        return "File"
    except IOError:
        f = html2text.html2text(urllib.request.urlopen(filename).read().decode("UTF-8"))
        print(f)
        return "Url"

# file = sys.argv[1]
file = 'http://www.usaco.org/current/data/sol_homework_silver_dec17.html'
file = "https://boggle.wordsmuggler.com/b/MLSTEAEFNONCTCAN"
print(checkFile(file))