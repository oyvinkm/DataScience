import cleaner
import pandas as pd
import itertools 
import numpy as np
df = cleaner.cleaner('news_sample.csv', 10)
allTags = []
allMeta = []
allAuthors = []
for i in range(len(df.index)):
    line = str(df['tags'].iloc[i]).lower().split(', ')
    line2 = str(df['meta_keywords'].iloc[i]).lower().split(', ')
    line3 = str(df['authors'].iloc[i]).lower().split(', ')
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
        row = {'tagID': 'NULL', 'articleID': articleId}
        articleTagList.append(row)
    else:
        article_tags = article_tags.lower().split(', ')
        for tag in article_tags:        
            tagId = int(tagDict[tag])
            row = {'tagID': tagId, 'articleID': articleId}
            articleTagList.append(row)

    if isinstance(meta_keys, float):
        row = {'meta_keyID': 'NULL', 'articleID': articleId}
        metaKeyList.append(row) 
    else: 
        meta_keys = meta_keys.lower().split(', ') 
        for keyword in meta_keys:
            keyID = metaDict[keyword]
            row = {'meta_keyID': keyID, 'articleID': articleId}
            metaKeyList.append(row)

    if isinstance(author_s, float):
        row = {'authorID': 'NULL', 'articleID': articleId}
        authorIdList.append(row) 
    else: 
        author_s = author_s.lower().split(', ') 
        for author in author_s:
            authorId = authorDict[author]
            row = {'authorID': authorId, 'articleID': articleId}
            authorIdList.append(row)


authorFrame = pd.DataFrame(list(authorDict.items()), columns = ['name', 'authorID'])
tagFrame = pd.DataFrame(list(tagDict.items()), columns = ['tag', 'tagID'])
keyFrame = pd.DataFrame(list(metaDict.items()), columns = ['meta_keyword', 'meta_keyID'])
authorFrame.to_csv('author_name.csv')
tagFrame.to_csv('tag_tag.csv')
keyFrame.to_csv('key_id_word.csv')


article_tag = pd.DataFrame(articleTagList)
article_tag.to_csv('article_tag.csv')

article_metaKey = pd.DataFrame(metaKeyList)
article_metaKey.to_csv('met_key_article.csv')

authorIdFrame = pd.DataFrame(authorIdList)
authorIdFrame.to_csv('authorID.csv')




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
Articles.rename(columns={"id" : "articleID"}, inplace=True)
Articles.to_csv('articles.csv')

TimeStamps = pd.DataFrame.from_dict(timeDict, orient='index', columns=['timeID'])
TimeStamps.to_csv('timestamps.csv')


types = pd.DataFrame(list(typeDict.items()), columns = ['type', 'typeID'])
types.to_csv('Types.csv')

DomainTypes = df[['domain','domainID', 'typeID']].copy()
DomainTypes.drop_duplicates(keep=False, inplace=True)
DomainTypes.to_csv('domain_types.csv')

Domains = df[['id','domainID']].copy()
Domains.rename(columns={"id":"articleID"}, inplace=True)
Domains.to_csv('domains.csv')



