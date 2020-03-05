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


typedict_1 = df.type.drop_duplicates().to_dict()
domaindict_1 = df.domain.drop_duplicates().to_dict()
scrapeDict_1 = df.scraped_at.drop_duplicates().to_dict()
insertDict_1 = df.inserted_at.drop_duplicates().to_dict()
updatedDict_1 = df.updated_at.drop_duplicates().to_dict()

scrapeDict = {y:x for x,y in scrapeDict_1.items()}
insertDict = {y:x for x,y in insertDict_1.items()}
updatedDict = {y:x for x,y in updatedDict_1.items()}
timeDict = {**scrapeDict, **insertDict, **updatedDict}
i = 1 
for key  in timeDict:
    timeDict[key] = i*3
    i += 1 
typeDict = {y:x for x,y in typedict_1.items()}
domainDict = {y:x for x,y in domaindict_1.items()}

df['typeID'] = df.apply(lambda row: typeDict[row['type']],axis = 1)
df['domainID'] = df.apply(lambda row: domainDict[row['domain']], axis = 1)
df['scrapedID'] = df.apply(lambda row: timeDict[row['scraped_at']], axis=1)
df['insertedID'] = df.apply(lambda row: timeDict[row['inserted_at']], axis=1)

TimeArticle = df[['id','scrapedID', 'insertedID']].copy()
TimeArticle.to_csv('time_article.cs')

domains = pd.DataFrame(list(domainDict.items()), columns = ['Domain', 'ID'])
domains.to_csv('Domains.csv')

types = pd.DataFrame(list(typeDict.items()), columns = ['Type', 'ID'])
types.to_csv('Types.csv')

TypeArticle = df[['id','typeID']].copy()
TypeArticle.to_csv('type_article.csv')

DomainArticle = df[['id','domainID']].copy()
DomainArticle.to_csv('domain_article.csv')


