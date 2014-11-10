# Luke Zhou, g3luke, 999079278

#!/usr/bin/env python
import sys

# TO UNCOMMENT IN THE FINAL SUBMISSION!!!!!!!!
#sys.path.append('/u/csc2501h/include/a4') 

# TO COMMENT OUT IN THE FINAL SUBMISSION!!!!!
sys.path.append('')

from Asst4 import nyt_big, nyt_mini #, DefaultNpPattern
# nyt_big  is the full POS-tagged 2004 NY Times corpus. 
# nyt_mini is the first 100K lines of nyt_big. 
# Use nyt_big for your final submission. You can use nyt_mini
# for testing and debugging your code during code development.
# DefaultNpPattern is a simple baseline pattern for NP chunking

from Asst4 import wn17 as wn
# Import version 1.7 of WordNet. 
# Newer versions will not work for Question 2!

from nltk.tree import Tree
from nltk.chunk.regexp import *
from HearstPatterns import *

# Save all hyponym suggestions in a text file
outfile = open("hyponyms.txt", "w") 

# IMPORT DECOY CORPUS
from Asst4 import decoyCorpus

print "==========================================="

# just for the purpose of illustration, print the output of the 
# NP Chunker for the first 3 sentences of nyt_mini
for s in decoyCorpus.tagged_sents(): #nyt_mini.tagged_sents()[0:1]:
	#print s
	
	try:
		NPChunked = NpChunker.parse(s)

		print stringify(NPChunked)

		doPattern1(NPChunked,outfile)
		doPattern2(NPChunked,outfile)
		doPattern3(NPChunked,outfile)
		doPattern4(NPChunked,outfile)
		doPattern5(NPChunked,outfile)

	except TypeError:
		#print 'FAIL'
		pass

	print "==========================================="

# also just for the purpose of illustration, print the synsets 
# for the word 'assignment'
''' for x in wn.synsets('assignment','n'):
    print x
'''


outfile.close()

