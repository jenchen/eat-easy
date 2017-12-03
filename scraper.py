#import selenium
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from random import randint
from time import sleep
from difflib import SequenceMatcher
import pandas as pd

class Scraper():
	"""
	Searches AllMenus.com for a restaurant's menu items and corresponding descriptions.
	"""
	def __init__(self, restuarant_name, restuarant_addr):
		self.site = 'https://www.allmenus.com'
		self.wait_time = 10 #60
		self.restuarant_name = restuarant_name
		self.restuarant_addr = restuarant_addr
		self.sleep_min = 0 #3
		self.sleep_max = 1 #7
		self.data = []

	def startBrowser(self):
		self.browser = webdriver.PhantomJS()
		self.browser.implicitly_wait(self.wait_time)
		#self.browser.get(self.site)

	def searchRestuarant(self):
		print('Starting search...')
		self.browser.get(self.site)
		search_field = self.browser.find_element(By.ID, 'get-address')
		search_field.clear()
		search_field.send_keys(self.restuarant_addr)
		print('Sleeping...')
		sleep(randint(self.sleep_min, self.sleep_max))
		search_field.send_keys(Keys.RETURN)
		print('Sleeping...')
		sleep(randint(self.sleep_min, self.sleep_max))

	def selectRestaurantFromResults_working(self):
		print('Selecting desired restuarant from search results...')
		lst_results = self.browser.find_elements(By.CSS_SELECTOR, 'h4.name a')
		restuarant_href = None
		for result in lst_results:
			print('RESULT')
			print(result)
			print('href')
			print(result.get_attribute('href'))
			if not isinstance(result, type(None)):
				possible_href = result.get_attribute('href')
				if possible_href and self.restuarant_name.lower().replace(' ', '-') in possible_href:
					restuarant_href = possible_href
					break
		
		print('Sleeping...')
		sleep(randint(self.sleep_min, self.sleep_max))
		self.browser.get(restuarant_href)

	def selectRestaurantFromResults(self): ######
		print('Selecting desired restuarant from search results...')
		lst_results = self.browser.find_elements(By.CSS_SELECTOR, 'h4.name a')
		restuarant_href = None
		for result in lst_results:
			if not isinstance(result, type(None)):
				possible_href = result.get_attribute('href')
				if possible_href and self.restuarant_name.lower().replace(' ', '-') in possible_href:
					restuarant_href = possible_href
					break
		if restuarant_href:
			print('Sleeping...')
			sleep(randint(self.sleep_min, self.sleep_max))
			self.browser.get(restuarant_href)
		return restuarant_href

	def similar(self, a, b):
		return SequenceMatcher(None, a, b).ratio()

	def pairMenuItemsAndDescriptions(self):
		print('Pairing menu items with their corresponding descriptions...')
		#menu_items = []
		resulting_menu_items = self.browser.find_elements(By.CLASS_NAME, 'item-title')
		#item_descriptions = []
		resulting_item_descriptions = self.browser.find_elements(By.CSS_SELECTOR, 'p.description')
		#prices = []
		resulting_prices = self.browser.find_elements(By.CLASS_NAME, 'item-price')
		for i in range(len(resulting_menu_items)):
			#menu_items.append(resulting_menu_items[i].text)
			#item_descriptions.append(resulting_item_descriptions[i].text)
			#prices.append(resulting_prices[i].text)
			##directly add to info_dict
			info_dict = {
				'rest_name': self.restuarant_name,
				'menu_item': resulting_menu_items[i].text,
				'description': resulting_item_descriptions[i].text,
				'price': resulting_prices[i].text
			}
			self.data.append(info_dict)
		#return [(menu_items[i], item_descriptions[i], prices[i]) for i in range(len(menu_items))]

	def write_to_csv(self):
		print("Writing to csv...")
		scraper_data = pd.DataFrame(columns=['rest_name', 'menu_item', 'description', 'price'], dtype=str) ##id
		scraper_data = scraper_data.append(self.data, ignore_index=True)
		scraper_data.to_csv('scraper_data.csv')

	def closeBrowser(self):
		if self.browser:
			self.browser.quit()

def print_output():
	print(restuarant_name)
	print(restuarant_addr)
	print("Num menu items: ", len(menu))
	for i in range(len(menu)):
		print(menu[i][0])
		print(menu[i][1])
		print(menu[i][2])

restuarant_name = 'House of Curries'
restuarant_addr = '2520 Durant Ave, Berkeley, CA, 94704' #2520
scraper = Scraper(restuarant_name, restuarant_addr)
scraper.startBrowser()
scraper.searchRestuarant()
success = scraper.selectRestaurantFromResults()
if success:
	scraper.pairMenuItemsAndDescriptions() #menu = 
	#print_output()
scraper.closeBrowser()
scraper.write_to_csv()

