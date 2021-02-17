# Author: 	jhenrie
# Date:		02/13/2020
# Description:	Process large set of text files and bin by character counts
# Notes:	Files can be found through wget https://www.cs.cmu.edu/~./enron/enron_mail_20150507.tar.gz

import re
import random
import subprocess
import os.path
import time
import sys

if len(sys.argv) > 1:
  ans = sys.argv[1]
else:
  ans = None

def pathMap(directory,output='/tmp/path-find-results.txt'):
  global ans
  # Prompt for overwrite if directory already exists
  if os.path.isfile(output):
    if ans == None:
      ans = raw_input('File for storing results already exists. Perform new search and overwrite (\'y\' or \'n\')?\n')
    if ans != 'y':
      return
  # Call linux find in directory and save to tmp file.
  subprocess.call('find '+directory+' -type f > '+output,shell=True)
  print('Searched '+directory+' and saved results to '+output)

def letterCount(s):
  strLower = s.lower()
  letters = []
  counts = []
  for i in 'abcdefghijklmnopqrstuvwxyz':
    letters.append(i)
    counts.append(len(re.findall(i,strLower)))
  return letters, counts

def letterCountMap(s):
  # TODO(jhenrie): Make a faster method using maps
  strLower = s.lower()
  letters = []
  counts = []
  letterFindall = re.findall('[a-z]',strLower)
  for i in 'abcdefghijklmnopqrstuvwxyz':
    letters.append(i)
    counts.append(len(re.findall(i,strLower)))
  return letters, counts
  pass

def sortByArray(list0, list1, sortBy=0, do_reverse=True):
  zipped = zip(list0, list1)
  sortedZip = sorted(zipped, key = lambda x: x[sortBy],reverse=do_reverse)
  return [i for i,j in sortedZip], [j for i,j in sortedZip]

"""
# Test letterCount over random
x = ''
for i in range(1000):
  x += chr(random.randrange(ord('a'),ord('z')+1))
letters, counts = letterCount(x)
for i,j in zip(letters, counts):
  print i,j
"""

"""
# Test sorting function
print("Testing sortByArray.")
numbers = [random.randrange(100) for i in range(26)]
letters = [chr(random.randrange(ord('a'),ord('z')+1)) for i in range(26)]
numbersSorted, lettersSorted = sortByArray(numbers,letters)
for idx,j in enumerate(numbersSorted):
  print j, lettersSorted[idx]
"""

"""
# Sort letter counts and print
zipped = zip(letters,counts)
sortedZip = sorted( zip(letters, counts), key = lambda x: x[1], reverse=True)

for i,j in sortedZip:
  print i,j
"""

# Perform directory mapping
pathMap('/usr/local/google/home/jhenrie/enron')

# Initialize letter count arrays
letters = [chr(i) for i in range(ord('a'),ord('z')+1)]
counts = [0]*len(letters)
totalChars = 0

# Get file list
with open('/tmp/path-find-results.txt') as f:
  fileNames = f.readlines()

print 'Files in directory: %s.' % '{:,}'.format(len(fileNames))
print 'Starting file processing.'

startTime = time.time()
filesRead = 0

# Loop through file list and update letter count arrays
for f in fileNames[:1000]:
  f = f.rstrip('\r\n')		# Fix filename formatting
  filesRead += 1		# Track file count

  # Read file contents
  with open(f) as currentF:
    s = currentF.read()
  totalChars += len(s)          # Account for latest file character count

  # Get file letter counts
  ltrsLatest, cntsLatest = letterCount(s)
  
  #print('Processed %d characters (%d letters) from "%s"' %(len(s),sum(cntsLatest),f) )

  # Include new counts on array
  for i in ltrsLatest:
    counts[letters.index(i)] += cntsLatest[letters.index(i)]

endTime = time.time()

# Sort results by character count
sortedLetters, sortedNumbers = sortByArray(letters,counts,1)

# Display results
totalLetters = sum(sortedNumbers)
for i,j in zip(sortedLetters,sortedNumbers):
  print '%s %4.1f%% %10s' %(i, float(j)/totalLetters*100, '{:,}'.format(j))

print('\nAll characters: %s\tLetters: %s (%.1f%% of all characters)' % ('{:,}'.format(totalChars), '{:,}'.format(totalLetters), float(totalLetters)/totalChars*100))
print('Read %s files in %.1f seconds (%.1f microseconds per file).' %('{:,}'.format(filesRead), endTime - startTime,(endTime - startTime)/filesRead*1E6))
