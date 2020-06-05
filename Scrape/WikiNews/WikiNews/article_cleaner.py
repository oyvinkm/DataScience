import numpy as np
import pandas as pd 
import re
from htmllaundry import strip_markup
#import execquery
import sklearn.feature_extraction.text as sk
import os
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
re4 = re.compile(r'[\d]{1,2}-[\d]{1,2}-[\d]{2,4}')
re5 = re.compile(r'[\d]{1,2}/[\d]{1,2}/[\d]{2,4}')
re6 = re.compile(r'[\d]{1,2} [\d]{1,2} [\d]{2,4}')
re7 = re.compile(r'[\d].{1,2}.[\d]{1,2}.[\d]{2,4}')
re8 = re.compile(r'[mtwfs]\w*[,]? [adfjmnos]\w*[,]?[.]? [\d]{1,2}(th)?[,]? ([\d]{2,4})?')
finReg = [re8, re1, re2, re3, re4, re5, re6, re7]
def swapDates(line):
    for reg in finReg:
        line = re.sub(reg, ' <DATE> ', line)
    return line

#Function to find and replace numbers with <NUM>
pattern = r'[\d]+[,]?([\d]+)?'
def swapNumb(line):
    line = re.sub(pattern, ' <NUM> ', line)
    return line
def tdif(data):
    tagList = []
    tfidf = sk.TfidfVectorizer(max_features=len(data), use_idf=True)
    tfidf.fit_transform(data['content']).toarray()
    feature_names = np.array(tfidf.get_feature_names())
    for i in range(len(data.index)):
        responses = tfidf.transform([data['content'].iloc[i]])
        def get_top_tf_idf_words(response, top_n=2):
            sorted_nzs = np.argsort(response.data)[:-(top_n+1):-1]
            return feature_names[response.indices[sorted_nzs]]
        tagList.append(get_top_tf_idf_words(responses, 5))
    return tagList
    

def cleaner(rawData):
    pattern = re.compile(r'\s+')
    pattern2 = re.compile(r'^,+')
    for index, row in rawData.iterrows():
        row['content'] = strip_markup(str(row['content']))
        row['content'] = re.sub(pattern2, '', row['content'])
        row['content'] = row['content'].lower()
        row['content'] = re.sub(pattern, ' ', row['content'])
        row['content'] = swapUrl(row['content'])
        row['content'] = swapDates(row['content'])
        row['content'] = swapNumb(row['content'])
    listofTags = tdif(rawData)
    for lists in listofTags:
        for item in lists:
            item = item.replace('[', '')
            item = item.replace(']', '')
            item = item.replace('the', '')
    map(''.join, listofTags)
    rawData['tags'] = listofTags

parentPath = os.path.dirname(os.getcwd())
os.chdir(parentPath)
data = readData('filebla.csv')
cleaner(data)


data.to_csv('Articles_Politics_Conflict.csv')