X_train, X_test, y_train, y_test = train_test_split(df['Review'], df['Rating'], test_size=0.2)

vect = TfidfVectorizer().fit(X_train)

X_train_vectorised = vect.transform(X_train)
"""
pac = PassiveAggressiveClassifier(max_iter=150)
pac.fit(X_train_vectorised, y_train)

ypred = pac.predict(vect.transform(X_test))

from sklearn.metrics import accuracy_score, confusion_matrix
accuracy = accuracy_score(y_test, ypred)
print(f'Accuracy Score of Passive Aggresive Scassifier: {round(accuracy*100,2)}%') """


model = LogisticRegression(multi_class='multinomial')
model.fit(X_train_vectorised, y_train)

y_pred = model.predict(vect.transform(X_test))

print(y_pred)

f1score = f1_score(y_test, y_pred, average='micro')
print (f"Score: {f1score * 100} %") 