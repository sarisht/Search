import os
import re
from scipy.sparse import csc_matrix, linalg
from scipy.linalg import diagsvd
from numpy import dot
from optparse import OptionParser
import operator
import math
import heapq
parser = OptionParser()
parser.add_option("-z")
parser.add_option("-k")
parser.add_option("--dir")
parser.add_option("--doc_in")
parser.add_option("--doc_out")
parser.add_option("--term_in")
parser.add_option("--term_out")
parser.add_option("--query_in")
parser.add_option("--query_out")
(options, args) = parser.parse_args()
z= int(options.z)
k = int(options.k)
dir1 = options.dir
doc_in = options.doc_in
doc_out = options.doc_out
term_in = options.term_in
term_out = options.term_out
query_in = options.query_in
query_out = options.query_out

count = {}
files = os.listdir(dir1)
all_words = {}
all_docs = {}
all_titles = {}
wordcnt = 0
titlecnt = 0
total = 0
def cosine_similarity(v1,v2):
	sumxx, sumxy, sumyy = 0, 0, 0
	sumxy = dot(v1,v2)
	sumxx = dot(v1,v1)
	sumyy = dot(v2,v2)
	return sumxy/math.sqrt(sumxx*sumyy)	
def key_from_value(list, search):
	for key, value in list.iteritems():
		if value == search:
			return key
for filename in files:
	f = open(dir+filename,'r')
	content = f.read().split('\n',1)
	pattern = re.compile(r'\W+')
	words = pattern.split(content[1].lower())
	title = content[0]
	all_docs[title] = total
	total += 1
	for word in words:
		pair = (word, title)
		try:
			count[pair] += (1.0 )
		except:
			count[pair] = (1.0)
		if word not in all_words:
			all_words[word] = wordcnt
			wordcnt += 1
print hello
row = [all_words[value[0]] for value in count.keys()]
col = [all_docs[value[1]] for value in count.keys()]
m = csc_matrix((count.values(),(row,col)))
u, s, vt = linalg.svds(m, z, which = 'LM')
reconstructedMatrix= dot(dot(u,diagsvd(s,z,len(vt))),vt)
#doc_in = "C:/Users/Sarisht Wadhwa/Desktop/Studies/Assignment3/Sample I_O/doc_in.txt"
#doc_out = "C:/Users/Sarisht Wadhwa/Desktop/Studies/Assignment3/Sample I_O/doc_out_my.txt"
f = open(doc_in,'r')
doc_query = f.read().split('\n')
f = open(doc_out,'w')
for query in doc_query:
	cosineVdoc = {}
	if (query != ('')):
		col = all_docs[query]
		v1 = reconstructedMatrix[:,col]
		print v1
		for a2 in xrange(total):
			v2 = reconstructedMatrix[:,a2]
			cosineVdoc[a2] = cosine_similarity(v1,v2)
	results = (heapq.nlargest(k, cosineVdoc, key= cosineVdoc.get))
	for result in results: 
		f.write(key_from_value(all_docs,result))
		f.write(';\t')
	f.write('\n')

#term_in = "C:/Users/Sarisht Wadhwa/Desktop/Studies/Assignment3/Sample I_O/term_in.txt"
#term_out = "C:/Users/Sarisht Wadhwa/Desktop/Studies/Assignment3/Sample I_O/term_out_my.txt"
f = open(term_in,'r')
term_query = f.read().split('\n')
f = open(term_out,'w')
for query in term_query:
	cosineVterm = {}
	if (query != ('')):
		row = all_words[query]
		v1 = reconstructedMatrix[row,:]
		for a2 in xrange(wordcnt):
			v2 = reconstructedMatrix[a2,:]
			cosineVterm[a2] = cosine_similarity(v1,v2)
	results = (heapq.nlargest(k, cosineVterm, key= cosineVterm.get))	
	for result in results: 
		f.write(key_from_value(all_words,result))
		f.write(';\t')
	f.write('\n')
	
#query_in = "C:/Users/Sarisht Wadhwa/Desktop/Studies/Assignment3/Sample I_O/query_in.txt"
#query_out = "C:/Users/Sarisht Wadhwa/Desktop/Studies/Assignment3/Sample I_O/query_out_my.txt"
f = open(query_in,'r')
query_query = f.read().split('\n')
f = open(query_out,'w')
for query in query_query:
	cosineVquery = {}
	if (query != ('')):
		v1 = [0]*wordcnt
		for word in query.split(" "):
			index = all_words[word]
			v1[index] = query.count(word)
		for a2 in xrange(total):
			v2 = reconstructedMatrix[:,a2]
			cosineVquery[a2] = cosine_similarity(v1,v2)
		results = (heapq.nlargest(k, cosineVquery, key= cosineVterm.get))	
		for result in results: 
			f.write(key_from_value(all_docs,result))
			f.write(';\t')
		f.write('\n')