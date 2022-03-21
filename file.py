import pandas as pd
from numpy import *
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import f1_score
from sklearn.linear_model import PassiveAggressiveClassifier
from nettoyage import *
from sklearn.model_selection import cross_val_score
from sklearn.metrics import accuracy_score
from nltk.util import ngrams


def nettoyerDataframe(df):
    df["Review"] = df.Review.map(lambda x: remove_URL(x))
    df["Review"] = df.Review.map(lambda x: remove_html(x))
    df["Review"] = df.Review.map(lambda x: remove_emoji(x))
    df["Review"] = df.Review.map(lambda x: remove_punct(x)) 
    df["Review"] = df.Review.map(remove_stopwords)   
    return df



def tfidf(df,ngrams):
    vect = TfidfVectorizer(ngram_range=ngrams).fit(df["Review"])
    X = vect.transform(df["Review"])
    return X



df = pd.read_csv('tripadvisor_hotel_reviews.csv')

df['Rating'] = df['Rating'].map({1:0, 2:0, 3:1, 4:1, 5:1})

df = nettoyerDataframe(df)

X = tfidf(df,(1,1))

y=df['Rating']


X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)


#Regression logistique
logisticRegression = LogisticRegression(multi_class='multinomial')
logisticRegression.fit(X_train, y_train)
y_pred = logisticRegression.predict(X_test)

print("\n***** Métriques d'évaluation : Regression logistique ******")
f1score = f1_score(y_test, y_pred, average='micro')
accuracy = accuracy_score(y_test, y_pred)
print (f"Score: {f1score * 100} %") 
print(f"Accuracy : {accuracy * 100} %")


#Naives Bayes
from sklearn.naive_bayes import GaussianNB

gaussianNB = GaussianNB()
gaussianNB.fit(X_train.toarray(),y_train)

y_pred = logisticRegression.predict(X_test)

print("\n***** Métriques d'évaluation : Naives Bayes ******")
f1score = f1_score(y_test, y_pred, average='micro')
accuracy = accuracy_score(y_test, y_pred)
print (f"Score: {f1score * 100} %") 
print(f"Accuracy : {accuracy * 100} %")


#SVM
from sklearn import svm

svmModel = svm.SVC(kernel='linear') # Linear Kernel
svmModel.fit(X_train, y_train)

y_pred = svmModel.predict(X_test)
print("\n***** Métriques d'évaluation : SVM ******")
f1score = f1_score(y_test, y_pred, average='micro')
accuracy = accuracy_score(y_test, y_pred)
print (f"Score: {f1score * 100} %") 
print(f"Accuracy : {accuracy * 100} %")






#Validation croisée sur le modèle de regression logfistique
scores = cross_val_score(logisticRegression, X, df["Rating"], cv=10)

print('Cross-Validation Accuracy Scores', scores)
scores = pd.Series(scores)
print(scores.min())
print(scores.mean())
print(scores.max())

"""
pac = PassiveAggressiveClassifier(max_iter=150)
pac.fit(X_train_vectorised, y_train)

ypred = pac.predict(vect.transform(X_test))

from sklearn.metrics import accuracy_score, confusion_matrix
accuracy = accuracy_score(y_test, ypred)
print(f'Accuracy Score of Passive Aggresive Scassifier: {round(accuracy*100,2)}%') 
"""
