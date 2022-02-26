import re
from time import sleep
import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver


def parse_html(html):
    data, item = pd.DataFrame(), {}
    soup = BeautifulSoup(html, 'lxml')

    for i, resto in enumerate(soup.find_all('div', class_='rest-row-info')):

        item['names'] = resto.find('span', class_='rest-row-name-text').text

        item['cuisine'] = resto.find('span', class_='rest-row-meta--cuisine rest-row-meta-text sfx1388addContent').text

        item['price'] = int(resto.find('div', class_='rest-row-pricing').find('i').text.count('£'))

        reviews = resto.find('span', class_='underline-hover')
        item['reviews'] = int(re.search('\d+', reviews.text).group()) if reviews else 'NA'

        rating = resto.find('div', class_='star-rating-score')
        item['rating'] = float(rating['aria-label'].split()[0]) if rating else 'NA'

        booking = resto.find('div', class_='booking')
        item['bookings'] = re.search('\d+', booking.text).group() if booking else 'NA'

        item['address'] = resto.find('span', class_='rest-row-meta--location rest-row-meta-text sfx1388addContent').text

        #url issue
        #url = resto.find('a', class_='rest-row-name rest-name')
        #item['url'] = re.search('(?P<url>https?://[^\s]+)', url.text) if url else 'NA'

        data[i] = pd.Series(item)

    return data.T


driver = webdriver.Safari()
url ="https://www.opentable.co.uk/london-restaurant-listings"
driver.get(url)
page = collected = 0

while page < 4:
    sleep(1)
    new_data = parse_html(driver.page_source)
    if new_data.empty:
        break
    if page == 0: # update the path
        new_data.to_csv('/Users/alyafattah/Desktop/results.csv', index=False)
    elif page > 0:
        new_data.to_csv('/Users/alyafattah/Desktop/results.csv', index=False, header=None, mode='a')
    page += 1
    collected += len(new_data)
    print(f'Page: {page} | Downloaded: {collected}')
    try:
        driver.find_element_by_link_text('Next').click()
    except:
        print("End")

driver.close()
restaurants = pd.read_csv('/Users/alyafattah/Desktop/results.csv')
print(restaurants)