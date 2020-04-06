import cleaner
import pandas as pd
import itertools
import parallel_clean
import numpy as np


df = cleaner.readData('1mio-raw.csv', 20000)
#rawData = cleaner.readData('news_sample.csv', 10)
#df = parallel_clean.parallelize_dataframe(rawData, cleaner.cleaner)
allTags = []
allMeta = []
allAuthors = []
for i in range(len(df.index)):
    line = str(df['tags'].iloc[i]).lower()
    line2 = str(df['meta_keywords'].iloc[i]).lower()
    line3 = str(df['authors'].iloc[i]).lower()
    line, line2, line3 = line.replace('[', ''), line2.replace('[', ''), line3.replace('[', '')
    line, line2, line3 = line.replace(']', ''), line2.replace(']', ''), line3.replace(']', '')
    line, line2, line3 = line.split(', '), line2.split(', '), line3.split(', ')
    allAuthors.append(line3)
    allMeta.append(line2)
    allTags.append(line)
allAuthors = (list(itertools.chain.from_iterable(allAuthors)))
allTags = (list(itertools.chain.from_iterable(allTags)))
allMeta= (list(itertools.chain.from_iterable(allMeta)))
authorList = list(dict.fromkeys(allAuthors))
metaList = list(dict.fromkeys(allMeta))
tagList = list(dict.fromkeys(allTags))
tagDict = {}
for i in range (len(tagList)):
    tagDict[tagList[i]] = i
metaDict = {}
for i in range (len(metaList)):
    metaDict[metaList[i]] = i
authorDict = {}
for i in range (len(authorList)):
    authorDict[authorList[i]] = i


articleTagList = []
metaKeyList = []
authorIdList = []

for i in range(len(df.index)):
    article_tags = df['tags'].iloc[i]
    meta_keys = df['meta_keywords'].iloc[i]
    articleId = df['id'].iloc[i]
    author_s = df['authors'].iloc[i]
    if isinstance(article_tags, float):
        row = {'tagID': 0, 'articleID': articleId}
        articleTagList.append(row)
    else:
        article_tags = article_tags.lower().split(', ')
        for tag in article_tags:  
            tag = tag.replace('[', '')
            tag = tag.replace(']', '')      
            tagId = int(tagDict[tag])
            row = {'tagID': tagId, 'articleID': articleId}
            articleTagList.append(row)

    if isinstance(meta_keys, float):
        row = {'meta_keyID': 0, 'articleID': articleId}
        metaKeyList.append(row) 
    else: 
        meta_keys = meta_keys.lower().split(', ') 
        for keyword in meta_keys:
            keyword = keyword.replace('[', '')
            keyword = keyword.replace(']', '')  
            keyID = metaDict[keyword]
            row = {'meta_keyID': keyID, 'articleID': articleId}
            metaKeyList.append(row)

    if isinstance(author_s, float):
        row = {'authorID': 'NULL', 'articleID': articleId}
        authorIdList.append(row) 
    else: 
        author_s = author_s.lower().split(', ') 
        for author in author_s:
            author = author.replace('[', '')
            author = author.replace(']', '')  
            authorId = authorDict[author]
            row = {'authorID': authorId, 'articleID': articleId}
            authorIdList.append(row)

authorDict = {y:x for x,y in authorDict.items()}
tagDict = {y:x for x,y in tagDict.items()}
metaDict = {y:x for x,y in metaDict.items()}
authorFrame = pd.DataFrame(list(authorDict.items()), columns = ['authorID', 'name'])
tagFrame = pd.DataFrame(list(tagDict.items()), columns = ['tagID', 'tag'])
keyFrame = pd.DataFrame(list(metaDict.items()), columns = ['meta_keyword', 'meta_keyID'])
authorFrame.to_csv('author_name.csv', index=False)
tagFrame.to_csv('tag_tag.csv', index=False)
keyFrame.to_csv('key_id_word.csv', index=False)


article_tag = pd.DataFrame(articleTagList)
article_tag.to_csv('article_tag.csv', index=False)

article_metaKey = pd.DataFrame(metaKeyList)
article_metaKey.to_csv('met_key_article.csv', index=False)

authorIdFrame = pd.DataFrame(authorIdList)
authorIdFrame.to_csv('authorID.csv', index=False)



df['type']=df['type'].fillna('NULL')
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


df['domainID'] = df.apply(lambda row: domainDict[row['domain']], axis = 1)
df['typeID'] = df.apply(lambda row: typeDict[row['type']], axis= 1)
df['scrapedID'] = df.apply(lambda row: timeDict[row['scraped_at']], axis=1)
df['insertedID'] = df.apply(lambda row: timeDict[row['inserted_at']], axis=1)
df['updatedID'] = df.apply(lambda row: timeDict[row['updated_at']], axis= 1)

Articles = df[['id', 'title','url','content','summary','scrapedID', 'insertedID', 'updatedID', 'meta_description']].copy()
Articles.rename(columns={"id" : "articleID"}, inplace=True)
Articles.to_csv('articles.csv', index=False)

timeDict = {y:x for x,y in timeDict.items()}
TimeStamps = pd.DataFrame(list(timeDict.items()), columns=['timeID', 'timestamp'], )
TimeStamps.to_csv('timestamps.csv', index=False)

typeDict = {y:x for x,y in typeDict.items()}
types = pd.DataFrame(list(typeDict.items()), columns = ['typeID', 'type'])
types.to_csv('Types.csv', index=False)

DomainTypes = df[['domainID','domain', 'typeID']].copy()
DomainTypes.drop_duplicates(subset='domainID', inplace=True)
DomainTypes.to_csv('domain_types.csv', index=False)

Domains = df[['id','domainID']].copy()
Domains.rename(columns={"id":"articleID"}, inplace=True)
Domains.to_csv('domains.csv', index=False)



