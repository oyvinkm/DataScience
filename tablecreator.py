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
        row = {'tagId': 'NULL', 'articleId': articleId}
        articleTagList.append(row)
    else:
        article_tags = article_tags.lower().split(', ')
        for tag in article_tags:        
            tagId = int(tagDict[tag])
            row = {'tagId': tagId, 'articleId': articleId}
            articleTagList.append(row)

    if isinstance(meta_keys, float):
        row = {'meta_key_id': 'NULL', 'articleId': articleId}
        metaKeyList.append(row) 
    else: 
        meta_keys = meta_keys.lower().split(', ') 
        for keyword in meta_keys:
            keyID = metaDict[keyword]
            row = {'meta_key_id': keyID, 'articleId': articleId}
            metaKeyList.append(row)

    if isinstance(author_s, float):
        row = {'authorId': 'NULL', 'articleId': articleId}
        authorIdList.append(row) 
    else: 
        author_s = author_s.lower().split(', ') 
        for author in author_s:
            authorId = authorDict[author]
            row = {'authorId': authorId, 'articleId': articleId}
            authorIdList.append(row)


authorFrame = pd.DataFrame(list(authorDict.items()), columns = ['Name', 'AuthorID'])
tagFrame = pd.DataFrame(list(tagDict.items()), columns = ['Tag', 'TagID'])
keyFrame = pd.DataFrame(list(metaDict.items()), columns = ['Keyword', 'Meta_keyID'])
authorFrame.to_csv('author_name.csv')
tagFrame.to_csv('tag_tag.csv')
keyFrame.to_csv('key_id_word.csv')


article_tag = pd.DataFrame(articleTagList)
article_tag.to_csv('article_tag.csv')

article_metaKey = pd.DataFrame(metaKeyList)
article_metaKey.to_csv('met_key_article.csv')

authorIdFrame = pd.DataFrame(authorIdList)
authorIdFrame.to_csv('authorID.csv')




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


