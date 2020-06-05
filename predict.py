import pandas as pd
import sklearn.feature_extraction.text as sk
import retrieve_data
from sklearn import svm
from sklearn.neighbors import KNeighborsClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn.ensemble import VotingClassifier

def train(data):
    vectorizer = sk.TfidfVectorizer(max_features=6000)
    X = vectorizer.fit_transform(data["content"]).toarray()
    Y = list(data["type"])
    clf_svm = svm.SVC(kernel='linear', class_weight='balanced', gamma='auto', probability=True)
    clf_svm.fit(X,Y)
    clf_kNeighbors = KNeighborsClassifier(n_neighbors = 30)
    clf_kNeighbors.fit(X,Y)
    clf_naiveBayes = GaussianNB()
    clf_naiveBayes.fit(X,Y)
    ensemble=VotingClassifier(estimators=[('SVM', clf_svm), ('naiveBayes', clf_naiveBayes), ('KNN', clf_kNeighbors)], 
                       voting='soft', weights=[1,1,1]).fit(X,Y)
    return ensemble

def predict(data, model, to_csv=False, targets=None, from_file=False):
    vectorizer = sk.TfidfVectorizer(max_features=6000)
    if (from_file):
        data = pd.read_csv(data)
        content_data = vectorizer.fit_transform(data["article"].values.astype('U')).toarray()
    else:
        content_data = vectorizer.fit_transform(data["content"]).toarray()
    labels = model.predict(content_data)
    if (to_csv):
        for i, y in enumerate(labels):
            if y == "reliable":
                labels[i] = "REAL"
            if y == "NULL":
                labels[i] = "FAKE"
            if y == "fake":
                labels[i] = "FAKE"
                
        data["label"] = labels
        id_with_predictions = data.drop("article", axis = 1)
        id_with_predictions.to_csv("predictions.csv", index=False)
    
    if (targets != None): 
        correct_counter = 0
        for i in range(len(targets)):
            if labels[i] == targets[i]:
                correct_counter += 1
        print("Number of test samples: {}".format(len(targets)))
        print("Model corrects: {}. Performance: {}".format(correct_counter, (correct_counter/len(targets))))
    