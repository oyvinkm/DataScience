import retrieve_data
from sklearn import svm
from sklearn.neighbors import KNeighborsClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn.tree import DecisionTreeClassifier
import sklearn.feature_extraction.text as sk

def baseline_performance(trainData, testData):
    vectorizer1 = sk.TfidfVectorizer(max_features=6000)
    X = vectorizer1.fit_transform(trainData["content"]).toarray()
    Y = list(trainData["type"])
    
    clf_svm = svm.SVC(kernel='linear', class_weight='balanced', gamma='auto', probability=True)
    clf_svm.fit(X,Y)
    clf_kNeighbors = KNeighborsClassifier(n_neighbors = 30)
    clf_kNeighbors.fit(X,Y)
    clf_naiveBayes = GaussianNB()
    clf_naiveBayes.fit(X,Y)
    clf_decisionTreee = DecisionTreeClassifier()
    clf_decisionTreee.fit(X,Y)

    vectorizer2 = sk.TfidfVectorizer(max_features=6000)
    test_content = vectorizer2.fit_transform(testData["content"]).toarray()
    real_types = list(testData["type"])

    Y1 = clf_svm.predict(test_content)
    Y2 = clf_kNeighbors.predict(test_content)
    Y3 = clf_naiveBayes.predict(test_content)
    Y4 = clf_decisionTreee.predict(test_content)

    correct_counter_svm = 0
    correct_counter_kNeigh = 0
    correct_counter_naiveBayes = 0
    correct_counter_decisionTree = 0
    for i in range(len(real_types)):
        if (real_types[i] == Y1[i]):
            correct_counter_svm += 1
        if (real_types[i] == Y2[i]):
            correct_counter_kNeigh += 1
        if (real_types[i] == Y3[i]):
            correct_counter_naiveBayes += 1
        if (real_types[i] == Y4[i]):
            correct_counter_decisionTree += 1
    
    print("Number of test samples: {}".format(len(real_types)))
    print("SVM corrects: {}. Performance: {}".format(correct_counter_svm, (correct_counter_svm/len(real_types))))
    print("KNeighbors corrects: {}. Performance: {}".format(correct_counter_kNeigh, (correct_counter_kNeigh/len(real_types))))
    print("NaiveBayes corrects: {}. Performance: {}".format(correct_counter_naiveBayes, (correct_counter_naiveBayes/len(real_types))))
    print("DecisionTree corrects: {}. Performance: {}".format(correct_counter_decisionTree, (correct_counter_kNeigh/len(real_types))))
