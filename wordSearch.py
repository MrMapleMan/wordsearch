
import sys
from re import findall as fa
import time

if len(sys.argv) < 3:
  print "Usage: python wordSearch.py letter_bank word_format\nWord format example: ....y."
elif len(sys.argv) > 3:
  print "Error: only 2 arguments should be included, letters and match pattern."
  sys.exit()

def checkWord(wrd, ltrs):
  for i in wrd:
    try:
      ltrs.remove(i)
    except:
      try:
        ltrs.remove('+')
      except:
        return False
  return True

def findMatches(pattern):
  matches = []

  print "re pattern: %s" %pattern
  words = fa(pattern,txt)
  words = list(set(words))
  print "Possible matches: %d" %len(words)
  for i in words[:5]:
    print i
  if len(words) > 5:
    print '...'
  
  for word in words:
    if checkWord(word, [i for i in letters]):
      matches.append(word)
  matches = set(matches)
  print "Matches:"
  for i in matches:
    print i
  
  print "%d matches" % len(matches)
  return matches
  #print "Num words: %d" %len(fa('\n',txt))

letters = [i for i in sys.argv[1]]
puzzle = sys.argv[2]
letters += fa('[a-z]', puzzle)
print "letters: %s" %''.join(letters)

patterns = []
alphabet = '[a-zA-Z]'
if not '*' in puzzle:
  patterns = ''.join([alphabet if i=='.' else i for i in puzzle])
else:
  for i in puzzle:
    # TODO: Figure out what to do here
    if i == '*':
      for cycle in range(2):
        patterns = patterns + [j+alphabet for j in patterns]
      #setOne = [j + alphabet for j in patterns]
      #setTwo = [j + alphabet*2 for j in patterns]
      #patterns = setOne + setTwo
    else:
      patterns = [j+i for j in patterns]

if len(patterns[0]) > 1:
  patterns = ['\\b'+i+'\\b' for i in patterns]
else:
  patterns = '\\b'+patterns+'\\b'

with open('words.txt') as f:
  txt = f.read()

findMatches(patterns)
