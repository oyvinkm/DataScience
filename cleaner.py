import numpy as np
import pandas as pd 
import re
import nltk
from nltk.tokenize import TweetTokenizer, ToktokTokenizer
from collections import Counter 
import itertools
import matplotlib as plt
import csv
#Function to read csv

def readData(path, size):
    chunklist = []
    df_chunk = pd.read_csv(path, sep=',', error_bad_lines=False, index_col=False, 
        dtype={'id':np.int32}, chunksize = size)
    for chunk in df_chunk:
        chunklist.append(chunk)
    return pd.concat(chunklist)

#Function to find and replace URLs with <URL>
urlPattern = r'((http|https)\:\/\/)?[a-zA-Z0-9\.\/\?\:@\-_=#]+\.([a-zA-Z]){2,6}([a-zA-Z0-9\.\&\/\?\:@\-_=#])*'
def swapUrl(line):
    line = re.sub(urlPattern,' <URL> ', line)
    return line

#Function to find and replace dates with <DATE>
re1 = re.compile(r'[\d]{1,2}(th)? [adfjmnos]\w*[,]?[.]? ([\d]{2,4})?')
re2 = re.compile(r'[adfjmnos]\w*[,]?[.]? [\d]{1,2}(th)?[,]? ([\d]{2,4})?')
re3 = re.compile(r'[adfjmnos]\w* [\d]{1,2}[,]?[.]?([\d]{2,4})?')
re4 = re.compile(r'[\d]{1,2}-[\d]{1,2}-[\d]{2,4}')
re5 = re.compile(r'[\d]{1,2}/[\d]{1,2}/[\d]{2,4}')
re6 = re.compile(r'[\d]{1,2} [\d]{1,2} [\d]{2,4}')
re7 = re.compile(r'[\d].{1,2}.[\d]{1,2}.[\d]{2,4}')
finReg = [re1, re2, re3, re4, re5, re6, re7]
def swapDates(line):
    for reg in finReg:
        line = re.sub(reg, ' <DATE> ', line)
    return line

#Function to find and replace numbers with <NUM>
pattern = r'[\d]+[,]?([\d]+)?'
def swapNumb(line):
    line = re.sub(pattern, ' <NUM> ', line)
    return line

def cleaner(csv, size):
    rawData = readData(csv, size)
    token = TweetTokenizer()
    stringList = []
    for line in rawData['content']:
        line = str(line)
        line = line.lower()
        pattern = re.compile(r'\s+')
        line = re.sub(pattern, ' ', line)
        line = line.rstrip('\n')
        line = swapUrl(line)
        line = swapDates(line)
        line = swapNumb(line)
        stringList.append(line)
        #tokenizedList.append(token.tokenize(line))
    rawData['content'] = stringList
    metaList = []
    for line in rawData['meta_keywords']:
        if (line ==  "['']"):
            metaList.append(np.nan)
        else: 
            metaList.append(line)
    rawData['meta_keywords'] = metaList
    return rawData

