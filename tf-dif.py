import execquery
import pandas as pd
import sklearn.feature_extraction.text as sk
from sklearn import svm
from sklearn.neighbors import KNeighborsClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn.ensemble import VotingClassifier


data = execquery.execQuery("""SELECT contents, articleID FROM articles Where articleid < 1000;""")
dataTypes = execquery.execQuery("""SELECT typen from typer NATURAL JOIN (SELECT typeID FROM domains NATURAL JOIN (SELECT domainID from articledomains where articleID < 1000) as foo) as foobar;""")
rawData = pd.DataFrame(data, columns=["content", "articleID"])
rawTypes = pd.DataFrame(dataTypes, columns=["type"])
rawData["type"] = rawTypes["type"]
vectorizer = sk.TfidfVectorizer(max_features=3000)
X = vectorizer.fit_transform(rawData["content"]).toarray()
#print(vectorizer.get_feature_names())
Y = list(rawData["type"])
clf_svm = svm.SVC(kernel='linear', class_weight='balanced', gamma='auto', probability=True)
clf_svm.fit(X,Y)
#clf_kNeighbors = KNeighborsClassifier(n_neighbors = 5)
#clf_kNeighbors.fit(X,Y)
clf_naiveBayes = GaussianNB()
clf_naiveBayes.fit(X,Y)
ensemble=VotingClassifier(estimators=[('SVM', clf_svm), ('naiveBayese', clf_naiveBayes)], 
                       voting='soft', weights=[1,2]).fit(X,Y)

testData = execquery.execQuery("""SELECT contents, articleID FROM articles Where articleID Between 1000 and 2000;""")
testDataRaw = pd.DataFrame(testData, columns=["content", "articleID"])
testTypes = execquery.execQuery("""SELECT typen from typer NATURAL JOIN (SELECT typeID FROM domains NATURAL JOIN (SELECT domainID from articledomains where articleID between 1000 and 2000) as foo) as foobar;""")
testRawTypes = pd.DataFrame(testTypes, columns=["type"])
vectorizer1 = sk.TfidfVectorizer(max_features=3000)
X1 = vectorizer1.fit_transform(testDataRaw["content"]).toarray()
Y1 = list(testRawTypes["type"])
Y2 = clf_svm.predict(X1)
#Y3 = clf_kNeighbors.predict(X1)
Y4 = clf_naiveBayes.predict(X1)
Y5 = ensemble.predict(X1)

#print(Y1)
#print(Y2)
#print(Y4)

correct_counter_svm = 0
correct_counter_kNeigh = 0
correct_counter_naiveBayes = 0
correct_counter_ensemble = 0
for i in range(len(Y1)):
    if (Y1[i] == Y2[i]):
        correct_counter_svm += 1
    #if (Y1[i] == Y3[i]):
     #   correct_counter_kNeigh += 1
    if (Y1[i] == Y4[i]):
        correct_counter_naiveBayes += 1
    if (Y4[i] == Y5[i]):
        correct_counter_ensemble += 1
print(correct_counter_svm)
print(correct_counter_kNeigh)
print(correct_counter_naiveBayes)
print(correct_counter_ensemble)