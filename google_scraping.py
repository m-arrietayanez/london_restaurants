from bs4 import BeautifulSoup
from splinter import Browser
from selenium import webdriver
import pandas as pd
import time
import sys
import json
import dateparser 
import requests
import lxml
from lxml import html
from lxml import etree
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys



#We will be using a dictionary that resembles our main table. 
restaurants = {}
restaurants["names"] = []
restaurants["summary"] = []
restaurants["cusine"] = []
restaurants["price"] = []
restaurants["reviews_count"] = []
restaurants["rating"] = []
restaurants["address"] = []
restaurants["url"] = []


def go_next_first_time():
    """Function to go from one restaurant to the next in Google Maps using Keyboard Control"""
    N = 9  # number of times you want to press TAB

    actions = ActionChains(browser) 
    #Press Tab Key
    actions.send_keys(Keys.TAB * N)
    actions.send_keys(Keys.SPACE)
    actions.perform()
    time.sleep(3)


def go_next():
    """Function to go from one restaurant to the next in Google Maps using Keyboard Control"""
    N = 2  # number of times you want to press TAB

    actions = ActionChains(browser) 
    #Press Tab Key
    actions.send_keys(Keys.TAB * N)
    actions.send_keys(Keys.SPACE)
    actions.perform()
    time.sleep(3)

def scrape_rest_info():
    """"Function to scrape relevant restaurant information from Google Maps and store data in a distionary of lists"""
    restaurants["names"].append(browser.find_element_by_class_name("x3AX1-LfntMc-header-title-title").text)
    try:
        restaurants["cusine"].append(browser.find_element_by_xpath("""//*[@id="pane"]/div/div[1]/div/div/div[2]/div[1]/div[1]/div[2]/div/div[2]/span[1]/span[1]/button""").text)
    except:
        restaurants["cusine"].append("Not a restaurant")
    
    try:
        restaurants['summary'].append(browser.find_element_by_xpath('//*[@id="pane"]/div/div[1]/div/div/div[6]/button/div/div[1]/div[1]/span').text)
    except:
        restaurants['summary'].append('NA')
    try:
        restaurants["price"].append(browser.find_elements_by_xpath("""//*[@id="pane"]/div/div[1]/div/div/div[2]/div[1]/div[1]/div[2]/div/div[1]/span[1]/span/span[2]/span[2]/span[1]/span""")[0].text)
    except IndexError:
        restaurants["price"].append("Not Available")
    
    try:
        restaurants["rating"].append(browser.find_element_by_class_name("aMPvhf-fI6EEc-KVuj8d").text)
    except:
        restaurants["rating"].append("Not Available")
    try:
        restaurants["reviews_count"].append(browser.find_element_by_class_name("Yr7JMd-pane-hSRGPd").text)
    except:
        restaurants["reviews_count"].append("NA")
    try:
        restaurants["address"].append(browser.find_elements_by_class_name("QSFF4-text")[0].text)
    except:
        restaurants["address"].append("NA")    
    restaurants["url"].append(browser.current_url)



###PERFORMING SCRAPE###
#Getting the base url
## Links in Google maps can be customized through queries: https://developers.google.com/maps/documentation/urls/get-started
###Forming the Search URL -> https://www.google.com/maps/search/?api=1&parameters
####Based on this, our base url is https://www.google.com/maps/search/?api=1&query=restaurants+in+london+uk
browser = webdriver.Chrome(ChromeDriverManager().install())
browser.get('https://www.google.com/maps/search/?api=1&query=restaurants+in+london+uk')
time.sleep(5)
#The first pop up we get is to accept or customize cookies. Here, we will simply accept them by 
##clicking on the xpath of the 'agree' button
browser.find_element_by_xpath('//*[@id="yDmH0d"]/c-wiz/div/div/div/div[2]/div[1]/div[4]/form/div/div/button').click()
browser.find_element_by_xpath('//*[@id="pane"]/div/div[1]/div/div/div[2]/div[1]/div[7]/div/a').click()
time.sleep(3)


#restaurants["address"].append(browser.find_element_by_xpath('//*[@id="pane"]/div/div[1]/div/div/div[9]/div[1]/button/div[1]/div[2]/div[1]').text)
counter = 0
page = 1
while page < 30:
    if counter == 0 and page == 1:
        scrape_rest_info()
        
        #Change focus to lower pane
        #Wait until item appears before clicking
        WebDriverWait(browser, 20).until(EC.presence_of_element_located((By.XPATH, '//*[@id="sGi9mc-m5SR9c-bottom-pane"]/div/div[1]/div/div/div/div[2]/div[1]')))
        browser.find_element_by_xpath('//*[@id="sGi9mc-m5SR9c-bottom-pane"]/div/div[1]/div/div/div/div[2]/div[1]').click()
        go_next_first_time()
        counter += 1
    elif counter == 0 and page > 1:
        #Wait until item appears before clicking
        time.sleep(10)
        #Click on first restaurant below ads
        browser.find_element_by_xpath('//*[@id="pane"]/div/div[1]/div/div/div[2]/div[1]/div[7]/div/a').click()
        time.sleep(5)
        #Get restaurant info
        scrape_rest_info()
        #Change focus to lower pane
        WebDriverWait(browser, 20).until(EC.presence_of_element_located((By.XPATH, '//*[@id="sGi9mc-m5SR9c-bottom-pane"]/div/div[1]/div/div/div/div[2]/div[1]')))
        browser.find_element_by_xpath('//*[@id="sGi9mc-m5SR9c-bottom-pane"]/div/div[1]/div/div/div/div[2]/div[1]').click()
        go_next_first_time()
        counter += 1

    elif counter < 18 and page > 0:
        go_next()
    ###All Restaurants after the first###
        time.sleep(5)
        scrape_rest_info()
        
        counter += 1
    elif counter == 18 and page > 0:
        #Go back
        browser.find_element_by_xpath('//*[@id="omnibox-singlebox"]/div[1]/div[1]/button').click()
    #Go to next page
        WebDriverWait(browser, 20).until(EC.presence_of_element_located((By.XPATH, '//*[@id="ppdPk-Ej1Yeb-LgbsSe-tJiF1e"]')))
        browser.find_element_by_xpath('//*[@id="ppdPk-Ej1Yeb-LgbsSe-tJiF1e"]').click()
    #Start over
        counter = 0
        page += 1
        print("You moved to page" + str(page))
    

browser.close()



##Convert dictionary to Pandas df
scraped_data_df = pd.DataFrame.from_dict(restaurants)


#Export to CSV
scraped_data_df.to_csv("data_google_maps.csv", index=False)    