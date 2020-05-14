import execquery
import pandas as pd
import sklearn.feature_extraction.text as sk
from sklearn import svm


data = execquery.execQuery("""SELECT contents, articleID FROM articles Where articleid < 1000;""")
dataTypes = execquery.execQuery("""SELECT typen from typer NATURAL JOIN (SELECT typeID FROM domains NATURAL JOIN (SELECT domainID from articledomains where articleID < 1000) as foo) as foobar;""")
rawData = pd.DataFrame(data, columns=["content", "articleID"])
rawTypes = pd.DataFrame(dataTypes, columns=["type"])
rawData["type"] = rawTypes["type"]
vectorizer = sk.TfidfVectorizer(max_features=3000)
X = vectorizer.fit_transform(rawData["content"]).toarray()
#print(vectorizer.get_feature_names())
Y = list(rawData["type"])
clf = svm.SVC(kernel='linear', class_weight='balanced', gamma='auto')
clf.fit(X,Y)

testData = execquery.execQuery("""SELECT contents, articleID FROM articles Where articleID Between 1000 and 2000;""")
testDataRaw = pd.DataFrame(testData, columns=["content", "articleID"])
testTypes = execquery.execQuery("""SELECT typen from typer NATURAL JOIN (SELECT typeID FROM domains NATURAL JOIN (SELECT domainID from articledomains where articleID between 1000 and 2000) as foo) as foobar;""")
testRawTypes = pd.DataFrame(testTypes, columns=["type"])
vectorizer1 = sk.TfidfVectorizer(max_features=3000)
X1 = vectorizer1.fit_transform(testDataRaw["content"]).toarray()
Y1 = list(testRawTypes["type"])
Y2 = clf.predict(X1)

print(Y1)
print(Y2)

correct_counter = 0
for i in range(len(Y1)):
    if (Y1[i] == Y2[i]):
        correct_counter += 1
print(correct_counter)