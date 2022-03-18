import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import f1_score
from nettoyage import *

def nettoyerDataframe(df):
    df["text"] = df.Review.map(lambda x: remove_URL(x))
    df["text"] = df.Review.map(lambda x: remove_html(x))
    df["text"] = df.Review.map(lambda x: remove_emoji(x))
    df["text"] = df.Review.map(lambda x: remove_punct(x)) 
    df["text"] = df.Review.map(remove_stopwords)   
    return df


def tfidf(data, ngrams=(1, 1)):
    # use_idf=False
    #sublinear_tf=True
    tfidf_vectorizer = TfidfVectorizer(ngram_range=ngrams)
    train = tfidf_vectorizer.fit_transform(data)
    return train, tfidf_vectorizer


df = pd.read_csv('tripadvisor_hotel_reviews.csv')

df=nettoyerDataframe(df)


train_tfidf, xxx = tfidf(df["Review"])

X = train_tfidf.todense()[0:][0:].tolist()

X_train, X_test, y_train, y_test = train_test_split(X, df['Rating'], test_size=0.2)

#vect = TfidfVectorizer().fit(X_train)

#X_train_vectorised = vect.transform(X_train)


model = LogisticRegression(multi_class='multinomial')
model.fit(X_train, y_train)

y_pred = model.predict(X_test)

print(y_pred)

f1score = f1_score(y_test, y_pred, average='micro')
print (f"Score: {f1score * 100} %")

