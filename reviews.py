import numpy as np
import requests
from bs4 import BeautifulSoup as soup
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import f1_score


"""
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

test = model.predict(vect.transform(["I really hated your product, it's bad!"]))

print(test)
"""


df = pd.DataFrame()
reviews = []
ratings = []


for cmp in range(0,125,5):

    url = "https://www.tripadvisor.com/Hotel_Review-g187147-d1172735-Reviews-or"+str(cmp)+"-Hotel_Liberty-Paris_Ile_de_France.html#REVIEWS"

    headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36'}

    page = requests.get(url, headers=headers)

    soup1 = soup(page.content, "html.parser")

    soup2 = soup(soup1.prettify(),'html.parser')



    list_reviews = soup2.findAll('q', {'class': 'XllAv H4 _a'})
    list_ratings = soup2.findAll('div', {'class' : 'emWez F1'})
    list_data_reviews = soup2.findAll('div', {'class': 'cqoFv _T'})



    for data_review in list_data_reviews:
        review = data_review.find('q',{'class':'XllAv H4 _a'})
        rating = data_review.find('div',{'class':'emWez F1'})
        reviews.append(review.find('span').text.strip())
        ratings.append(rating.find('span').attrs['class'][1][7])




df['Reviews'] = reviews
df['Ratings'] = ratings

print(df)