import csv
import os
import praw
import string
import unicodedata
import sys

# function for setting up praw

def setuppraw():
	
	reddit = praw.Reddit('bot1')
	subreddit = reddit.subreddit(input('what sub to count? '))
	print()
	print('counting words in /r/' + str(subreddit))
	
	return subreddit

# function for checking if a file containing a word count already 
# exists in the same dir as this script

def loadfile():
	
	if not os.path.isfile('foundwords.csv'):
		founddata = []
		print('Made a new foundwords.csv')
		print()
	
	else:
		infile = open('foundwords.csv')
		inreader = csv.reader(infile)
		founddata = list(inreader)
		print('using existing foundwords.csv')
		print()
	return founddata
	
# this code removes the punctuation from the words that are found

tbl = dict.fromkeys(i for i in range(sys.maxunicode)
if unicodedata.category(chr(i)).startswith('P'))
                      
def removepunctuation(text):
    return text.translate(tbl)
    
# function for making a list out of each post to check against the 
# words already in the word count file 
  
def loadpost():
	postwords = []
	subreddit = setuppraw()
	howmany = input('How many posts should I read? ')
	for submission in subreddit.hot(limit=int(howmany)):
		for word in submission.selftext.split():
			word = removepunctuation(word)
			word = word.lower()
			postwords.append(word)
	return postwords
	
def postvsfile(postlist, filelist):
	for word in postlist:
		if word not in [item[0] for item in filelist]:
			filelist.append([word,'1'])
			print("added " + word + " to list")
		else:
			index = int([item[0] for item in filelist].index(word))
			filelist[index][1] = int(filelist[index][1]) + 1
			
			
	return filelist
	
def writefile(founddata):
	outfile = open('foundwords.csv', 'w', newline = '')
	outwriter = csv.writer(outfile)
	
	for row in founddata:
		outwriter.writerow(row)
	outfile.close


filedata = postvsfile(loadpost(), loadfile())
print('Words in csv file: ', len(filedata))

writefile(filedata)
	
	
