import requests 
from flask import Flask, request, jsonify, make_response
import random
from flask import Flask, request, Blueprint, render_template, redirect, session
from  selenium import webdriver
from bs4 import BeautifulSoup
import smtplib
import time
from lxml.html import fromstring
import requests
from itertools import cycle
import traceback
from datetime import datetime
import itertools
import re
import csv
import json
#from selenium.webdriver.common.by import By
#from config import config
from random import seed
from random import randint
import os
#import validators
from flask import url_for
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
import scrapy
from flask_httpauth import HTTPBasicAuth
auth = HTTPBasicAuth()

@auth.get_password
def get_password(username):
    if username == '':
        return 'python'
    return None

@auth.error_handler
def unauthorized():
    return make_response(jsonify({'error': 'Unauthorized access'}), 401)



############# analise for fake reviews
############# multithreaded scraping  
############# proxy rotation https://www.reddit.com/r/webscraping/comments/ab9huf/bye_bye_403_building_a_filter_resistant_web/
############# login & UI registration 





app = Flask(__name__)


def check_amazon_url(url):

    amz_url_regex = '/https?:\/\/(www|smile)\.amazon\.com\/(?:(?:[\w-]+\/)?(?:dp|gp\/product)\/(\w{10})\/)?/;'
    #'https?:\/\/(?=(?:....)?amazon|smile)(www|smile)\S+com(((?:\/(?:dp|gp)\/([A-Z0-9]+))?\S*[?&]?(?:tag=))?\S*?)(?:#)?(\w*?-\w{2})?(\S*)(#?\S*)+'

    if(re.search(amz_url_regex,url)):
        return True 
          
    else:
        return False 


def get_price(url):
    """Scrape page price."""
    price = None
    
    html = browser_connect(url)


    if html.find(id="priceblock_ourprice"):
        price = html.find(id="priceblock_ourprice").get_text()
    elif html.find(id="priceblock_dealprice"):
        price = html.find(id="priceblock_dealprice").get_txt()
    elif html.find(id="priceblock_saleprice"):
        price = html.find(id="priceblock_saleprice").get_txt()
    elif html.find(id="price_inside_buybox"):
        price = html.find(id="price_inside_buybox").get_txt()
    else:
        price = ""

    return price



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


   # for i in range(0,len(review_date)):
    fieldnames = zip(review_title, cust_name, rate, review_date_content, review_content)

#    print(fieldnames)
    fieldnames = {}
    fieldnames['id'] = names
    #fieldnames['text'] = 'dlfgkldfgkl'
    #fieldnames['cust_name'] = 'dlfgkldfgklfgdfgdfgdfgiei9393'

    #jsonStr = jsonify(rate)


    with open('reviews.csv', 'w', newline='') as csvfile:
      review_csv = csv.writer(csvfile, delimiter=',', quoting=csv.QUOTE_MINIMAL)
      review_csv.writerows(fieldnames)
          

    csvfile.close()

    print(fieldnames)
    return(fieldnames)


def get_review_date(url):

    soup = browser_connect(url)

    max_page_number = soup.find(attrs={'data-hook': 'total-review-count'}).text.strip()

    review_date = soup.find_all("span",{"data-hook":"review-date"})

    review_date_content = []
    
    for i in range(0,len(review_date)):
      review_date_content.append(review_date[i].get_text())

    #review_date_content[:] = [review_date.lstrip('\n') for review_date in review_date_content]

    return(review_date_content)



def get_rating(url):

    soup = browser_connect(url)

    max_page_number = soup.find(attrs={'data-hook': 'total-review-count'}).text.strip()

    rating = soup.find_all('i',class_='review-rating')

    rate = []

    for i in range(0,len(rating)):
      rate.append(rating[i].get_text())

    return(rate)


def get_content(url):

    soup = browser_connect(url)

    max_page_number = soup.find(attrs={'data-hook': 'total-review-count'}).text.strip()

    #find all elements

    review = soup.find_all("span",{"data-hook":"review-body"})

    review_content = []
    
    for i in range(0,len(review)):
      review_content.append(review[i].get_text())

    review_content[:] = [reviews.lstrip('\n') for reviews in review_content]


    return(review_content)



def get_title(url):

    #url = "https://www.amazon.com/dp/" + asin + "#customerReviews"

    soup = browser_connect(url)

    max_page_number = soup.find(attrs={'data-hook': 'total-review-count'}).text.strip()

    #find all elements

    title = soup.find_all('a',class_='review-title-content')
    
    review_title = []

    for i in range(0,len(title)):
      review_title.append(title[i].get_text())

    review_title[:] = [titles.lstrip('\n') for titles in review_title]

    return(review_title)

def get_proxies():
    url = 'https://free-proxy-list.net/'
    response = requests.get(url)
    parser = fromstring(response.text)
    proxies = set()
    for i in parser.xpath('//tbody/tr')[:20]:
        if i.xpath('.//td[7][contains(text(),"yes")]'):
            proxy = ":".join([i.xpath('.//td[1]/text()')[0], i.xpath('.//td[2]/text()')[0]])
            proxies.add(proxy)
    return proxies


def proxy_test():

    proxies = get_proxies()
    proxy_pool = cycle(proxies)

    url = 'https://httpbin.org/ip'
    for i in range(1,20):
        #Get a proxy from the pool
        proxy = next(proxy_pool)
        print("Request #%d"%i)
        print(proxy)
        try:
            response = requests.get(url,proxies={"http": proxy, "https": proxy})
            print(response.json())
            vproxy = proxy
            return(vproxy)
        except:
            #Most free proxies will often get connection errors. You will have retry the entire request using another proxy to work. 
            #We will just skip retries as its beyond the scope of this tutorial and we are only downloading a single url 
            print("Skipping. Connnection error")

def browser_connect(url):

    ptest = proxy_test() 
    print(ptest)
    #headers = {'User-Agent': get_random_user_agent()}

    ua = get_random_user_agent()
    print(ua)
    options = webdriver.ChromeOptions()

    options.add_argument('--incognito')
    #options.add_argument('--headless')
    options.add_argument('--disable-extensions')
    options.add_argument('start-maximized')
    options.add_argument('disable-infobars')
    options.add_argument('--user-agent=' + ua)


    #options.add_argument("--proxy-server=http://%s" % ptest)
    options.add_argument("-proxy-server=http://" + ptest)
    #options.add_argument("-proxy-server=http://103.115.255.201:80" + ptest)
    
    print(url)
    
    #options.add_argument('user-agent=',headers)
        

    #browserdriver = webdriver.Chrome(ChromeDriverManager().install())

    browserdriver = webdriver.Chrome(options=options, executable_path=r'/Users/fabio.fanni/Downloads/chromedriver')

    response = browserdriver.get(url)

    content = browserdriver.page_source

    soup = BeautifulSoup(content, 'html.parser')

    browserdriver.quit()

    return soup 


@app.route('/review-date/<asin>', methods=['GET'])
#@auth.login_required
def review_date(asin):

    product_url = 'https://www.amazon.com/dp/' + asin

    output = get_review_date(product_url)

    return jsonify(output)



@app.route('/review-title/<asin>', methods=['GET'])
#@auth.login_required
def review_title(asin):

    product_url = 'https://www.amazon.com/dp/' + asin

    output = get_title(product_url)

    return jsonify(output)

@app.route('/review-content/<asin>', methods=['GET'])
#@auth.login_required

def review_content(asin):

    product_url = 'https://www.amazon.com/dp/' + asin

    output = get_content(product_url)

    return jsonify(output)


@app.route('/review-rating/<asin>', methods=['GET'])
#@auth.login_required

def review_rating(asin):

    product_url = 'https://www.amazon.com/dp/' + asin

    output = get_rating(product_url)

    return jsonify(output)

@app.route('/get-price/<asin>', methods=['GET'])
#@auth.login_required

def product_price(asin):

    product_url = 'https://www.amazon.com/dp/' + asin

    output = get_price(product_url)

    return jsonify(output)


@app.route('/proxy-test/', methods=['GET'])
#@auth.login_required

def p_test():

    test_url = 'http://fabio.io'


    output = get_price(test_url)

    return jsonify(output)



    
if __name__ == '__main__':
    app.run(debug=True)