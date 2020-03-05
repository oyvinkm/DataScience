import cleaner
import pandas as pd
import itertools 

df = cleaner.cleaner('news_sample.csv', 10)
allTags = []
allMeta = []
for i in range(len(df.index)):
    line = str(df['tags'].iloc[i])
    line2 = str(df['meta_keywords'].iloc[i])
    line2 = line2.split(', ')
    line = line.split(', ')
    allMeta.append(line2)
    allTags.append(line)
flatTag = (list(itertools.chain.from_iterable(allTags)))
flatMeta = (list(itertools.chain.from_iterable(allMeta)))
metaList = list(dict.fromkeys(flatMeta))
tagList = list(dict.fromkeys(flatTag))
tagDict = {}
for i in range (len(tagList)):
    tagDict[tagList[i]] = i
metaDict = {}
for i in range (len(metaList)):
    metaDict[metaList[i]] = i


typedict = df.type.drop_duplicates().to_dict()
domaindict = df.domain.drop_duplicates().to_dict()
scrapeDict = df.scraped_at.drop_duplicates().to_dict()
insertDict = df.inserted_at.drop_duplicates().to_dict()
updatedDict = df.updated_at.drop_duplicates().to_dict()

scrapeDict = {y:x for x,y in scrapeDict.items()}
insertDict = {y:x for x,y in insertDict.items()}
updatedDict = {y:x for x,y in updatedDict.items()}
timeDict = {**scrapeDict, **insertDict, **updatedDict}
i = 1 
for key  in timeDict:
    timeDict[key] = i*3
    i += 1 
typeDict = {y:x for x,y in typedict.items()}
domainDict = {y:x for x,y in domaindict.items()}

df['typeID'] = df.apply(lambda row: typeDict[row['type']],axis = 1)
df['domainID'] = df.apply(lambda row: domainDict[row['domain']], axis = 1)
df['scrapedID'] = df.apply(lambda row: timeDict[row['scraped_at']], axis=1)
df['insertedID'] = df.apply(lambda row: timeDict[row['inserted_at']], axis=1)
df['updatedID'] = df.apply(lambda row: timeDict[row['updated_at']], axis= 1)

TimeArticle = df[['id','scrapedID', 'insertedID', 'updatedID']].copy()
TimeArticle.to_csv('time_article.csv')

domains = pd.DataFrame(list(domainDict.items()), columns = ['Domain', 'ID'])
domains.to_csv('Domains.csv')

types = pd.DataFrame(list(typeDict.items()), columns = ['Type', 'ID'])
types.to_csv('Types.csv')

TypeArticle = df[['id','typeID']].copy()
TypeArticle.to_csv('type_article.csv')

DomainArticle = df[['id','domainID']].copy()
DomainArticle.to_csv('domain_article.csv')


