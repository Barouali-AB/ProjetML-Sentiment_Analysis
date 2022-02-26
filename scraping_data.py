import requests
from bs4 import BeautifulSoup as soup
import csv
import re


data = open(r'hotel_reviews.csv', 'w', encoding="utf-8", newline="")
writer = csv.writer(data)
header = ["Review", "Rating"]
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
        row = [review.find('span').text.strip(), rating.find('span').attrs['class'][1][7]]
        writer.writerow(row)






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




url = "https://www.tripadvisor.com/Hotels-g187147-Paris_Ile_de_France-Hotels.html"

page = requests.get(url, headers=headers)
soup1 = soup(page.content, "html.parser")
soup2 = soup(soup1.prettify(),'html.parser')

list_hotels = soup2.find('div', {'class':'relWrap'})
hotels = list_hotels.findAll('div', {'class':'prw_rup prw_meta_hsx_responsive_listing ui_section listItem'})

for hotel in hotels:

    link = hotel.find('a', {'class': 'property_title prominent'}, href=True)
    if (link):

        url_origin = "https://www.tripadvisor.com" + link['href']
        url = url_origin
        scrap_data(url)
        cmp = 0

        while (not last_page(url)):

            cmp += 5
            url = re.sub(r'(Reviews-)', "or" + str(cmp) + "-", url_origin)
            scrap_data(url)

            








