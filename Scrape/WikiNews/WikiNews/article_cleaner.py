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

def readData(path):
    data = pd.read_csv(path, sep=',', error_bad_lines=False, index_col=False)
    return data

#Function to find and replace URLs with <URL>
urlPattern = r'((http|https)\:\/\/)?[a-zA-Z0-9\.\/\?\:@\-_=#]+\.([a-zA-Z]){2,6}([a-zA-Z0-9\.\&\/\?\:@\-_=#])*'
def swapUrl(line):
    line = re.sub(urlPattern,' <URL> ', line)
    return line

#Function to find and replace dates with <DATE>
re1 = re.compile(r'[\d]{1,2}(th)? [adfjmnos]\w*[,]?[.]? ([\d]{2,4})?')
re2 = re.compile(r'[adfjmnos]\w*[,]?[.]? [\d]{1,2}(th)?[,]? ([\d]{2,4})?')
re3 = re.compile(r'[adfjmnos]\w* [\d]{1,2}[,]?[.]?([\d]{2,4})?')
re8 = re.compile(r'[mtwfs]\w*[,]?[adfjmnos]\w* ([\d]{2,4})?[,]?[.]? ([\d]{2,4})?')
re4 = re.compile(r'[\d]{1,2}-[\d]{1,2}-[\d]{2,4}')
re5 = re.compile(r'[\d]{1,2}/[\d]{1,2}/[\d]{2,4}')
re6 = re.compile(r'[\d]{1,2} [\d]{1,2} [\d]{2,4}')
re7 = re.compile(r'[\d].{1,2}.[\d]{1,2}.[\d]{2,4}')
finReg = [re1, re2, re3, re4, re5, re6, re7, re8]
def swapDates(line):
    for reg in finReg:
        line = re.sub(reg, ' <DATE> ', line)
    return line

#Function to find and replace numbers with <NUM>
pattern = r'[\d]+[,]?([\d]+)?'
def swapNumb(line):
    line = re.sub(pattern, ' <NUM> ', line)
    return line

def cleaner(rawData):
    #Removing rows with wrong articleId
    pattern = re.compile(r'\s+')
    #pattern2 = re.compile
    for index, row in rawData.iterrows():
        #seperator = ','
        #seperator.join(row['content'])
        row['content'] = str(row['content'])
        row['content'] = row['content'].lower()
        row['content'] = re.sub(pattern, ' ', row['content'])
        row['content'] = swapUrl(row['content'])
        row['content'] = swapDates(row['content'])
        row['content'] = swapNumb(row['content'])
    return rawData
data = readData('filebla.csv')
cleaner(data)
data.to_csv('WikiArticles.csv', index=False)