#!/usr/bin/env python
import sys

# TO UNCOMMENT IN THE FINAL SUBMISSION!!!!!!!!
#sys.path.append('/u/csc2501h/include/a4') 

# TO COMMENT IN THE FINAL SUBMISSION!!!!!
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

# Create a chunk parser with the default pattern for NPs
DefaultNpPattern = ''.join([r'(<DT|AT>?<RB>?)?',
			    r'<JJ.*|CD.*>*',
			    r'(<JJ.*|CD.*><,>)*',
			    r'(<N.*>)+'])
BaselineNpChunkRule = ChunkRule(DefaultNpPattern, 'Default rule for NP chunking')
NpChunker = RegexpChunkParser([BaselineNpChunkRule], chunk_node='NP',top_node='S')

# Create chunk parsers for each of Hearst's five lexicosyntactic patterns

"""
Pattern1 = ''.join([r'<NP>,?',r' such as ', 
				r'<NP>((, <NP>)*,?((and)|(or)) <NP>)?'])
Pattern1 = ''.join([r'<NP> such as <NP>'])
ChunkRule1 = ChunkRule(Pattern1, 'Rule #1')
Chunker1 = RegexpChunkParser([ChunkRule1], chunk_node='woot',top_node='S')
"""

Pattern1 = """ 	woot: {<NP><,>?<JJ><IN><NP>((<,><NP>)*<,>?<CC><NP>)?} 
						}<JJ><IN>{ 
						}<CC>{
						}<,>{ 
				suchP: {<JJ>}
				asP: {<IN>}
				conjP: {<CC>} """ 
Chunker1 = RegexpParser(Pattern1)

# Save all hyponym suggestions in a text file
outfile = open("hyponyms.txt", "w") 

# IMPORT DECOY CORPUS
from Asst4 import decoyCorpus

# just for the purpose of illustration, print the output of the 
# NP Chunker for the first 3 sentences of nyt_mini
for s in decoyCorpus.tagged_sents(): #nyt_mini.tagged_sents()[0:1]:
	#print s
	
	try:
		NPChunked = NpChunker.parse(s)
		Chunked1 = Chunker1.parse(NPChunked)
		Chunked1NPs = list(Chunked1.subtrees(lambda np: np.node=="woot"))

		for i in Chunked1.subtrees(lambda i: i.node=="suchP" or i.node=="asP" or i.node=="conjP"):
			nodeWord = i.leaves()[0][0]
			if(nodeWord!="such" and nodeWord!="as" and nodeWord!="and" and nodeWord!="or"):
				raise StopIteration

		FirstNP = Chunked1NPs[0].leaves()[0][0]

		for np in Chunked1NPs[1:len(Chunked1NPs)]:
			print FirstNP + ", " + np.leaves()[0][0]

			outfile.write(FirstNP + " " + np.leaves()[0][0] + '\n');

		outfile.write('\n')

	except TypeError:
		#print 'FAIL'
		pass
	except StopIteration:
		#print 'cock'
		pass


# also just for the purpose of illustration, print the synsets 
# for the word 'assignment'
''' for x in wn.synsets('assignment','n'):
    print x
'''


outfile.close()
