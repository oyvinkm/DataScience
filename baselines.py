import retrieve_data
from sklearn import svm
from sklearn.neighbors import KNeighborsClassifier
from sklearn.naive_bayes import GaussianNB, MultinomialNB
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import accuracy_score
from sklearn.metrics import classification_report
from sklearn.linear_model import SGDClassifier
from sklearn.ensemble import VotingClassifier, BaggingClassifier
import sklearn.feature_extraction.text as sk
import pandas as pd
import numpy as np

def baseline_performance(trainData, testData):
    vectorizer = sk.TfidfVectorizer(max_features=200, use_idf=True, stop_words='english')
    X = vectorizer.fit_transform(trainData["content"]).toarray()
    print(vectorizer.get_feature_names())
    test_content = vectorizer.transform(testData["content"]).toarray()
    real_types = list(testData["type"])

    Y = list(trainData["type"])
    
    clf_svm_linear = svm.SVC(kernel='linear', gamma='auto', probability=True)
    clf_svm_linear.fit(X,Y)
    clf_kNeighbors = KNeighborsClassifier(n_neighbors = 5, weights='distance')
    clf_kNeighbors.fit(X,Y)
    clf_MultiNB = MultinomialNB(alpha=0.1)
    clf_MultiNB.fit(X,Y)    

    Y2 = clf_kNeighbors.predict(test_content)
    Y3 = clf_svm_linear.predict(test_content)
    Y5 = clf_MultiNB.predict(test_content)

    print("Number of test samples: {}".format(len(real_types)))
    print("Linear SVM Accuracy: {}".format(accuracy_score(real_types, Y3)))
    print("Linear SVM classification report \n {}".format(classification_report(real_types,Y3)))
    print("KNeighbors Accuracy: {}".format(accuracy_score(real_types, Y2)))
    print("KNeighbors classification report \n {}".format(classification_report(real_types,Y2)))
    print("MultiNB Accuracy: {}".format(accuracy_score(real_types, Y5)))
    print("MultiNB classification report \n {}".format(classification_report(real_types,Y5)))
    