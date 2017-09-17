""" a simple python program to count the wourds in a subreddits posts
	there should be a praw.ini file in the same dir as this program
    leave the /r/ off of the reddit name, it is added by the script"""

#!/usr/bin/env python3
import csv
import os
import unicodedata
import sys
import praw

# function for setting up praw

def setuppraw():
    """ Looks for praw.ini and use it to set up praw."""
    reddit = praw.Reddit('bot1')
    subreddit = reddit.subreddit(input('what sub to count? '))
    print()
    print('counting words in /r/' + str(subreddit))

    return subreddit

# function for checking if a file containing a word count already
# exists in the same dir as this script

def loadfile():
    """ Look for the found words csv file, if there is one load it
        if there isnt one, make it. """
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

TBL = dict.fromkeys(i for i in range(sys.maxunicode)
                    if unicodedata.category(chr(i)).startswith('P'))

def removepunctuation(text):
    """ Return the word minus the punctuation."""
    return text.translate(TBL)

# function for making a list out of each post to check against the
# words already in the word count file

def loadpost():
    """ Return a list of the words in the posts self text. """
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
    """ Compair the words in the postlist with the words in the filelist
    if the word is already in the file list, load its point value and
    add one to it."""
    for word in postlist:
        if word not in [item[0] for item in filelist]:
            filelist.append([word, '1'])
            print("added " + word + " to list")
        else:
            index = int([item[0] for item in filelist].index(word))
            filelist[index][1] = int(filelist[index][1]) + 1

    return filelist

def writefile(founddata):
    """ Write the updated filelist list to the foundwords.csv file."""
    outfile = open('foundwords.csv', 'w', newline='')
    outwriter = csv.writer(outfile)

    for row in founddata:
        outwriter.writerow(row)

FILE_WORDS = postvsfile(loadpost(), loadfile())
print('Words in csv file: ', len(FILE_WORDS))

writefile(FILE_WORDS)
