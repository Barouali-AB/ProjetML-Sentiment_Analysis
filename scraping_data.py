import requests
from bs4 import BeautifulSoup as soup
import csv
import re


header = ["Review", "Rating"]

data = open(r'all_reviews.csv', 'w', encoding="utf-8", newline="")


writer = csv.writer(data)
writer.writerow(header)

headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36'}



def scrap_data(url):
    page = requests.get(url, headers=headers)
    soup1 = soup(page.content, "html.parser")
    soup2 = soup(soup1.prettify(), 'html.parser')

    list_data_reviews = soup2.findAll('div', {'class': 'cqoFv _T'})

    for data_review in list_data_reviews:

        review = data_review.find('q', {'class': 'XllAv H4 _a'})
        rating = data_review.find('div', {'class': 'emWez F1'})
        rating_value = rating.find('span').attrs['class'][1][7]
        if (int(rating_value) < 3):
            row = [review.find('span').text.strip(), rating_value]
            writer.writerow(row)

        else:
            continue


def number_reviews(url):
    page = requests.get(url, headers=headers)
    soup1 = soup(page.content, "html.parser")
    soup2 = soup(soup1.prettify(), 'html.parser')

    list_data_reviews = soup2.findAll('div', {'class': 'cqoFv _T'})
    return len(list_data_reviews)


def last_page(url):
    page = requests.get(url, headers=headers)
    soup1 = soup(page.content, "html.parser")
    soup2 = soup(soup1.prettify(), 'html.parser')
    pages = soup2.find('div', {'class':'pageNumbers'})
    current_page = pages.find('span', {'class':'pageNum current disabled'})
    current_page_num = int(current_page.text.strip())

    other_pages = pages.findAll('a',{'class':'pageNum'})
    list_other_pages = []
    for other_page in other_pages:
        list_other_pages.append(int(other_page.text.strip()))
    max_page = max(list_other_pages)

    if current_page_num < max_page :
        return False
    else :
        return True



url1 ="https://www.tripadvisor.com/Hotel_Review-g186338-d282814-Reviews-Abercorn_House-London_England.html"
url2 = "https://www.tripadvisor.com/Hotel_Review-g60763-d1181739-Reviews-The_Jane_Hotel-New_York_City_New_York.html"
url3 = "https://www.tripadvisor.com/Hotel_Review-g60763-d122005-Reviews-The_New_Yorker_A_Wyndham_Hotel-New_York_City_New_York.html"
url4 = "https://www.tripadvisor.com/Hotel_Review-g60763-d93627-Reviews-West_Side_YMCA-New_York_City_New_York.html"
url5 = "https://www.tripadvisor.com/Hotel_Review-g60763-d7182733-Reviews-The_Paul_Hotel_NYC-New_York_City_New_York.html"
url6 = "https://www.tripadvisor.com/Hotel_Review-g60763-d671150-Reviews-The_Empire_Hotel-New_York_City_New_York.html"
url7 = "https://www.tripadvisor.com/Hotel_Review-g60763-d142114-Reviews-Night_Hotel_Broadway-New_York_City_New_York.html"

urls = [ url1, url2, url3, url4, url5, url6, url7]

for url_origin in urls:
    
    url = url_origin
    scrap_data(url)
    cmp = 0
    while (not last_page(url) ):

        cmp += number_reviews(url)
        url = re.sub(r'(Reviews-)', "or" + str(cmp) + "-", url_origin)
        scrap_data(url)



