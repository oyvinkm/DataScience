import pandas as pd
import sklearn.feature_extraction.text as sk
import retrieve_data
from sklearn import svm
from sklearn.neighbors import KNeighborsClassifier
from sklearn.naive_bayes import GaussianNB, MultinomialNB
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import VotingClassifier
from sklearn.ensemble import BaggingClassifier
from sklearn.metrics import accuracy_score
from sklearn.metrics import classification_report

def model(trainData,testData):
    vectorizer = sk.TfidfVectorizer(max_features = 500, use_idf=True, stop_words='english')
    X = vectorizer.fit_transform(trainData["content"]).toarray()
    Y = list(trainData["type"])
    clf_svm = svm.SVC(C=1.0, kernel='rbf', class_weight='balanced', gamma=0.1, probability=True)
    clf_kNeighbors = KNeighborsClassifier(n_neighbors = 5, weights='distance')
    clf_MultiNB = MultinomialNB(alpha=0.1)
    ensemble = VotingClassifier(estimators=[('SVM', clf_svm), ('KNeighBors', clf_kNeighbors), ('MultiNB', clf_MultiNB)],weights=[1,1,1], voting='soft', n_jobs=-1)
    ensemble.fit(X,Y)
    #c_array= [0.01, 0.1, 1]

    # Best linear C=0.1
    # Best rbf C=1.0
    '''
    for c in c_array:
        clf_svm = svm.SVC(C=c,kernel='rbf', class_weight='balanced', gamma=0.1, probability=True)
        clf_svm.fit(X,Y)
        Y1 = clf_svm.predict(test_content)
        print("Number of test samples: {}. C-value={}".format(len(real_types),c))
        print("SVM Accuracy: {}".format(accuracy_score(real_types, Y1)))
        print("SVM classification report \n {}".format(classification_report(real_types,Y1)))    
    '''
    test_content = vectorizer.transform(testData["content"]).toarray()
    real_types = list(testData["type"])

    Y7 = ensemble.predict(test_content)


    print("Ensemble Accuracy: {}".format(accuracy_score(real_types, Y7)))
    print("Ensemble classification report \n {}".format(classification_report(real_types,Y7)))
    
    
    kaggle_data = pd.read_csv('test_data.csv')
    content_data = vectorizer.transform(kaggle_data["article"].values.astype('U')).toarray()
    labels = ensemble.predict(content_data)

    
    real_counter = 0
    fake_counter = 0
    for i, y in enumerate(labels):
        if y == "reliable":
            labels[i] = "REAL"
            real_counter += 1
        if y == "NULL":
            labels[i] = "FAKE"
            fake_counter += 1
        if y == "fake":
            labels[i] = "FAKE"
            fake_counter += 1
    print("Reals in Kaggle pred: {}".format(real_counter))
    print("Fakes in Kaggle pred: {}".format(fake_counter))
    kaggle_data["label"] = labels
    id_with_predictions = kaggle_data.drop("article", axis = 1)
    id_with_predictions.to_csv("predictions.csv", index=False)

    liar_data = pd.read_csv('liar_test.tsv', delimiter='\t')
    liar_content = vectorizer.transform(liar_data['content'].values.astype('U')).toarray()
    true_labels = liar_data['type']
    for i, y in enumerate(true_labels):
        if y == "true":
            true_labels[i] = "reliable"
        if y == "mostly-true":
            true_labels[i] = "reliable"
        else:
            true_labels[i] = "fake"
    
    pred_labels = ensemble.predict(liar_content)

    print("Ensemble Accuracy (Liar-Liar): {}".format(accuracy_score(true_labels, pred_labels)))
    print("Ensemble classification report (Liar-Liar) \n {}".format(classification_report(true_labels,pred_labels)))