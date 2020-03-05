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


typeDict = df.type.drop_duplicates().to_dict()
domainDict = df.domain.drop_duplicates().to_dict()
typeDict = {y:x for x,y in typeDict.items()}
domainDict = {y:x for x,y in domainDict.items()}

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

df['typeID'] = df.apply(lambda row: typeDict[row['type']],axis = 1)
df['domainID'] = df.apply(lambda row: domainDict[row['domain']], axis = 1)
df['scrapedID'] = df.apply(lambda row: timeDict[row['scraped_at']], axis=1)
df['insertedID'] = df.apply(lambda row: timeDict[row['inserted_at']], axis=1)
df['updatedID'] = df.apply(lambda row: timeDict[row['updated_at']], axis= 1)

Articles = df[['id', 'title','url','content','summary','scrapedID', 'insertedID', 'updatedID', 'meta_description']].copy()
Articles.to_csv('articles.csv')

TimeStamps = pd.DataFrame.from_dict(timeDict, orient='index', columns=['timeID'])
TimeStamps.to_csv('timestamps.csv')


types = pd.DataFrame(list(typeDict.items()), columns = ['Type', 'ID'])
types.to_csv('Types.csv')

DomainTypes = df[['domain','domainID', 'typeID']].copy()
DomainTypes.drop_duplicates(keep=False, inplace=True)
DomainTypes.to_csv('domain_types.csv')

Domains = df[['id','domainID']].copy()
Domains.to_csv('domains.csv')



