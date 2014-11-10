# Luke Zhou, g3luke, 999079278

from nltk.chunk.regexp import *

# Create a chunk parser for NPs
NpPattern = ''.join([r'(<DT|AT|PP>?)?',
			    r'<CD.*|JJ.*>*',
			    r'(<CD.*|JJ.*><,>)*',
			    r'(<N.*>)+'
			    ])
NpChunkRule = ChunkRule(NpPattern, 'Default rule for NP chunking')
NpChunker = RegexpChunkParser([NpChunkRule], chunk_node='NP',top_node='S')

# Turns a tree structure into a linearized string
def stringify(tree):
	toReturn = ''
	for n in tree.leaves():
		toReturn = toReturn + n[0] + ' '
	return toReturn[0:-1]

# Removes determinants and adjectives from an NP, 
# and returns a linearized string of the head
def NpHead(NPtree):

	"""for w in NPtree.leaves():
		print w
		if w[1]=="NN" or w[1]=="NP" or w[1]=="NNS" or w[1]=="NPS":
			return w[0]
	return stringify(NPtree)
	"""
	toBattle = NPtree.leaves()
	#print toBattle

	StripPattern = r"""	head: {(<N.*>)+}
			    	"""
	StripChunker = RegexpParser(StripPattern)
	StripChunked = StripChunker.parse(toBattle)

	#ChunkedHeads = list(StripChunked.subtrees(lambda np: np.node=="head"))

	toReturn = ''
	for i in StripChunked.subtrees(lambda i: i.node=="head"):
		toReturn = toReturn + stringify(i)

	return toReturn

# Create chunk parsers for each of Hearst's five lexicosyntactic patterns

###################################################
# TAKE CARE OF PATTERN 1
###################################################
Pattern1 = r""" woot: {<NP><,>?<JJ><IN><NP>((<,><NP>)*<,>?<CC><NP>)?} 
						}<JJ><IN>{ 
						}<CC>{
						}<,>{ 
				suchP: <woot><,>?{<JJ>}<IN>
				asP: <suchP>{<IN>}<woot>
				conjP: (<,><woot>)*<,>?{<CC>}<woot> """ 
Chunker1 = RegexpParser(Pattern1)

def doPattern1(NpChunked,outfile):
	Chunked1 = Chunker1.parse(NpChunked)
	Chunked1NPs = list(Chunked1.subtrees(lambda np: np.node=="woot"))

	#print Chunked1

	if len(Chunked1NPs)==0:
		return

	for i in Chunked1.subtrees(lambda i: i.node=="suchP" or i.node=="asP" or i.node=="conjP"):
		nodeWord = stringify(i)
		
		if(nodeWord!="such" and nodeWord!="as" and nodeWord!="and" and nodeWord!="or"):
			#print "gops" + nodeWord
			#raise StopIteration
			return

	print "Rule 1 applies!"
	FirstNP = NpHead(Chunked1NPs[0])

	# Write Hyponym(a,b) pairs to the file
	for np in Chunked1NPs[1:len(Chunked1NPs)]:
		print NpHead(np) + ", " + FirstNP

		outfile.write(NpHead(np) + ", " + FirstNP + '\n');
	outfile.write('\n')

###################################################
# TAKE CARE OF PATTERN 2
###################################################
Pattern2 = r""" woot: {<JJ><NP><IN><NP>((<,><NP>)*<,>?<CC><NP>)?} 
						}<JJ>{ 
						}<IN>{
						}<CC>{
						}<,>{ 
				suchP: {<JJ>}<woot>
				asP: <woot>{<IN>}<woot>
				conjP: (<,><woot>)*<,>?{<CC>}<woot>  """ 
Chunker2 = RegexpParser(Pattern2)

def doPattern2(NpChunked,outfile):
	Chunked2 = Chunker2.parse(NpChunked)

	#print Chunked2

	Chunked2NPs = list(Chunked2.subtrees(lambda np: np.node=="woot"))

	if len(Chunked2NPs)==0:
		return

	for i in Chunked2.subtrees(lambda i: i.node=="suchP" or i.node=="asP" or i.node=="conjP"):
		nodeWord =stringify(i)
		if(nodeWord!="such" and nodeWord!="as" and nodeWord!="and" and nodeWord!="or"):
			print
			#raise StopIteration
			return

	print "Rule 2 applies!"
	FirstNP = NpHead(Chunked2NPs[0])

	# Write Hyponym(a,b) pairs to the file
	for np in Chunked2NPs[1:len(Chunked2NPs)]:
		print NpHead(np) + ", " + FirstNP

		outfile.write(NpHead(np) + ", " + FirstNP + '\n');
	outfile.write('\n')

###################################################
# TAKE CARE OF PATTERN 3
###################################################
Pattern3 = r""" woot: {<NP>(<,><NP>)*<,>?<CC><JJ><NP>} 
						}<JJ>{
						}<CC>{
						}<,>{ 
				otherP: <CC>{<JJ>}<woot>
				conjP: {<CC>}<otherP>  """ 
Chunker3 = RegexpParser(Pattern3)

def doPattern3(NpChunked,outfile):
	Chunked3 = Chunker3.parse(NpChunked)

	#print Chunked3

	Chunked3NPs = list(Chunked3.subtrees(lambda np: np.node=="woot"))

	if len(Chunked3NPs)==0:
		return

	for i in Chunked3.subtrees(lambda i: i.node=="otherP" or i.node=="conjP"):
		nodeWord = stringify(i) #i.leaves()[0][0]
		if(nodeWord!="and" and nodeWord!="or" and nodeWord!="other"):
			print
			#raise StopIteration
			return

	print "Rule 3 applies!"
	LastNP = NpHead(Chunked3NPs[-1])

	# Write Hyponym(a,b) pairs to the file
	for np in Chunked3NPs[0:-1]:
		print NpHead(np) + ", " + LastNP		
		outfile.write(NpHead(np) + ", " + LastNP + '\n');
	
	outfile.write('\n')

###################################################
# TAKE CARE OF PATTERN 4
###################################################
Pattern4 = r""" woot: {<NP><,>?<VBG><NP>((<,><NP>)*<,>?<CC><NP>)?} 
						}<VBG>{
						}<CC>{
						}<,>{ 
				includingP: <NP><,>?{<VBG>}<,>?<woot>
				conjP: {<CC>}<woot>  """ 
Chunker4 = RegexpParser(Pattern4)

def doPattern4(NpChunked,outfile):
	Chunked4 = Chunker4.parse(NpChunked)

	#print Chunked4

	Chunked4NPs = list(Chunked4.subtrees(lambda np: np.node=="woot"))

	if len(Chunked4NPs)==0:
		return

	for i in Chunked4.subtrees(lambda i: i.node=="includingP" or i.node=="conjP"):
		nodeWord = stringify(i)
		if(nodeWord!="and" and nodeWord!="or" and nodeWord!="including"):
			print
			return

	print "Rule 4 applies!"
	FirstNP = NpHead(Chunked4NPs[0])

	# Write Hyponym(a,b) pairs to the file
	for np in Chunked4NPs[1:len(Chunked4NPs)]:
		print NpHead(np) + ", " + FirstNP		
		outfile.write(NpHead(np) + ", " + FirstNP + '\n');
	
	outfile.write('\n')

###################################################
# TAKE CARE OF PATTERN 5
###################################################
Pattern5 = r""" woot: {<NP><,>?<RB><NP>((<,><NP>)*<,>?<CC><NP>)?} 
						}<RB>{
						}<CC>{
						}<,>{ 
				especiallyP: <woot><,>?{<RB>}<,>?<woot>
				conjP: {<CC>}<woot>  """ 
Chunker5 = RegexpParser(Pattern5)

def doPattern5(NpChunked,outfile):
	Chunked5 = Chunker5.parse(NpChunked)

	#print Chunked5

	Chunked5NPs = list(Chunked5.subtrees(lambda np: np.node=="woot"))

	if len(Chunked5NPs)==0:
		return

	for i in Chunked5.subtrees(lambda i: i.node=="especiallyP" or i.node=="conjP"):
		nodeWord = stringify(i)
		if(nodeWord!="and" and nodeWord!="or" and nodeWord!="especially"):
			print
			return

	print "Rule 5 applies!"
	FirstNP = NpHead(Chunked5NPs[0])

	# Write Hyponym(a,b) pairs to the file
	for np in Chunked5NPs[1:len(Chunked5NPs)]:
		print NpHead(np) + ", " + FirstNP		
		outfile.write(NpHead(np) + ", " + FirstNP + '\n');
	
	outfile.write('\n')