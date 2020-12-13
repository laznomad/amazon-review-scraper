import requests 
import flask
import random
from flask import Flask, request, Blueprint, render_template, redirect, session
from  selenium import webdriver
from bs4 import BeautifulSoup
import smtplib
import time
from datetime import datetime
import itertools
import re
import csv
import json
#from selenium.webdriver.common.by import By
from config import config
from random import seed
from random import randint
import os
#import validators
from flask import url_for
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
import scrapy

def get_random_user_agent():
    
    user_agent_list = ['Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.103 Safari/537.36',
                       'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36',
                       'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.80 Safari/537.36',
                       'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.80 Safari/537.36',
                       'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36',
                       'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36',
                       'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36',
                       'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36',
                       'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36',
                       'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.67 Safari/537.36'
                       'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.67 Safari/537.36'
                       'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36',
                       'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.67 Safari/537.36',
                       'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36',
                       'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.67 Safari/537.36',
                       'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36',
                       'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.67 Safari/537.36']
    return random.choice(user_agent_list)



def get_reviews(url):

    #url = "https://www.amazon.com/dp/" + asin + "#customerReviews"

    soup = browser_connect(url)

    max_page_number = soup.find(attrs={'data-hook': 'total-review-count'}).text.strip()
    


    #find all elements

    names = soup.find_all('span',class_='a-profile-name')

    title = soup.find_all('a',class_='review-title-content')
    
    rating = soup.find_all('i',class_='review-rating')

    review = soup.find_all("span",{"data-hook":"review-body"})

    review_date = soup.find_all("span",{"data-hook":"review-date"})

    verified_purchase = soup.find_all("span",{"data-hook":"avp-badge"})


    #create arrays for each list of element and iterate

    review_content = []
    
    review_title = []

    rate = []

    cust_name = []

    review_date_content = []

    avp_badge = []
    
    #iterate reviews

    for i in range(0,len(review)):
      review_content.append(review[i].get_text())

    review_content[:] = [reviews.lstrip('\n') for reviews in review_content]


    #iterate review title

    for i in range(0,len(title)):
      review_title.append(title[i].get_text())

    review_title[:] = [titles.lstrip('\n') for titles in review_title]

    #iterate review ratings

    for i in range(0,len(rating)):
      rate.append(rating[i].get_text())


    #iterate name

    for i in range(0,len(names)):
      cust_name.append(names[i].get_text())


    #iterate review date 
    
    for i in range(0,len(review_date)):
      review_date_content.append(review_date[i].get_text())

    review_date_content[:] = [review_date.lstrip('\n') for review_date in review_date_content]


    #for i in range(0,len(review_date)):
    fieldnames = zip(review_title, cust_name, rate, review_date_content, review_content)

    with open('reviews.csv', 'w', newline='') as csvfile:
      review_csv = csv.writer(csvfile, delimiter=',', quoting=csv.QUOTE_MINIMAL)
      review_csv.writerows(fieldnames)
          

    csvfile.close()

      

def browser_connect(url):

    headers = {'User-Agent': get_random_user_agent()}

    options = webdriver.ChromeOptions()

    options.add_argument('--incognito')
    options.add_argument('--headless')
    options.add_argument('--disable-extensions')
    options.add_argument('start-maximized')
    options.add_argument('disable-infobars')
        

    browserdriver = webdriver.Chrome(ChromeDriverManager().install())

    #browserdriver = webdriver.Chrome(options=options, executable_path=r'/Users/nomad/Downloads/chromedriver')

    response = browserdriver.get(url)

    content = browserdriver.page_source

    soup = BeautifulSoup(content, 'html.parser')

    browserdriver.quit()

    return soup 


def main():

    print("Insert Amazon Product URL\n")
    
    url = input()

    get_reviews(url)
    
if __name__ == '__main__':


    main()
    