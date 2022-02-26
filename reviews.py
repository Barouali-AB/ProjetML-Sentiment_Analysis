
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import f1_score


df = pd.read_csv('tripadvisor_hotel_reviews.csv')

X_train, X_test, y_train, y_test = train_test_split(df['Review'], df['Rating'], test_size=0.2)

vect = TfidfVectorizer().fit(X_train)

X_train_vectorised = vect.transform(X_train)


model = LogisticRegression(multi_class='multinomial')
model.fit(X_train_vectorised, y_train)

y_pred = model.predict(vect.transform(X_test))

print(y_pred)

f1score = f1_score(y_test, y_pred, average='micro')
print (f"Score: {f1score * 100} %")

