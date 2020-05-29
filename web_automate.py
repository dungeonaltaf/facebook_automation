#!/usr/bin/python3
from selenium import webdriver
import urllib.request
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import  WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
import requests
from bs4 import BeautifulSoup
from selenium.common.exceptions import NoSuchElementException
import logging
import sys 
logging.basicConfig(filename='web_automate.log',level=logging.DEBUG,format='%(asctime)s %(levelname)s: %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p')

def connect(host='http://google.com'):
	try:
		urllib.request.urlopen(host) #Python 3.x
		return True
	except:
			return False

def scrap_website():
	quote_url = 'https://www.goodreads.com/quotes/recently_added'
	quote_response = requests.get(quote_url)
	soup = BeautifulSoup(quote_response.text,'lxml')
	quotes = soup.find_all('div',class_='quoteText')
	#authors = soup.find_all('span',class_='authorOrTitle')
	quote = quotes[0].text.strip('\n')
	#author = authors[0].text.strip('\n')
	return quote

def set_driver_options():
	option = Options()
	option.add_argument("--disable-infobars")
	option.add_argument('headless')
	option.add_argument('window-size=1200x600')
	option.add_argument("start-maximized")
	option.add_argument("--disable-extensions")
	option.add_experimental_option("prefs", { 
    "profile.default_content_setting_values.notifications": 2 
	})
	return option

def status_update(quote):
	option = set_driver_options()
	driver = webdriver.Chrome(chrome_options=option)
	driver.maximize_window()
	url = 'https://www.facebook.com/'
	driver.get(url)
	email_address = sys.argv[1]
	password = sys.argv[2]
	
	email_input = driver.find_element_by_xpath('//*[@id="email"]')
	email_input.send_keys(email_address)
	password_input = driver.find_element_by_xpath('//*[@id="pass"]')
	password_input.send_keys(password)
	log_in_btn = driver.find_element_by_xpath('//*[@id="u_0_b"]')
	log_in_btn.click()
		#delay = 100 # seconds
	driver.implicitly_wait(30)
		#status_delay = 50
	status_input = driver.find_element_by_name("xhpc_message")
	status_input.click()
	status_input.send_keys(quote)
	postBtn3 = driver.find_element_by_css_selector("button[class='_1mf7 _4r1q _4jy0 _4jy3 _4jy1 _51sy selected _42ft']")
	postBtn3.click()
	driver.implicitly_wait(60)
	account_settings = driver.find_element_by_id("userNavigationLabel")
	account_settings.click()
	logout_btn = driver.find_element_by_link_text("Log Out")
	logout_btn.click()
		#driver.quit() 

if connect():
	quote = scrap_website()
	status_update(quote)
else:
	print("No connectin")
#	logging.info('Network was not established')

