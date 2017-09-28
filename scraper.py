#import selenium
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from random import randint
from time import sleep

class Scraper():
	"""
	Searches AllMenus.com for a restaurant's menu items and corresponding descriptions.
	"""
	def __init__(self, restuarant_name, restuarant_addr):
		self.site = 'allmenus.com'
		self.wait_time = 60
		self.restuarant_name = restuarant_name
		self.restuarant_addr = restuarant_addr
		self.sleep_min = 3
		self.sleep_max = 7

	def startBrowser(self):
		self.browser = webdriver.PhantomJS()
		self.browser.implicitly_wait(self.wait_time)
		self.browser.get(self.site)
		##figure out how to deal with only online orders


	def searchRestuarant(self):
		print('Searching for desired restuarant...')
		search_field = self.browser.find_element(By.ID, 'get-address')
		search_field.clear()
		search_field.send_keys(self.restuarant_addr)
		print('Sleeping...')
		sleep(randint(self.sleep_min, self.sleep_max))
		search_field.send_keys(Keys.RETURN)
		##self.browser.find_element(By.CSS_SELECTOR, 'input.s-btn.s-button-primary').click() #submit button
		print('Sleeping...')
		sleep(randint(self.sleep_min, self.sleep_max))

		#submit form
		#select and send restuarant_addr to search box: css-selector by id: get-address
		#sleep for 3-5 sec
		#click submit button
		#sleep

	def selectRestaurantFromResults(self):
		print('Selecting desired restuarant from search results...')
		lst_results = self.browser.find_elements(By.CSS_SELECTOR, 'h4.name')
		restuarant = None
		for result in lst_results:
			if result.get_attribute('inner-html') == self.restuarant_name:
				restuarant = result
		print('Sleeping...')
		sleep(randint(self.sleep_min, self.sleep_max))
		restuarant.click() #


		##select actual restuarant
		#get everything by css selector: h4.name a where href="/ca/berkeley/309673-house-of-curries/menu/"
			#OR can try inner-html == restuarant_name (House Of Curries)
		#then click
		#sleep

	def pairMenuItemsAndDescriptions(self):
		print('Pairing menu items with their corresponding descriptions')
		menu_items = self.browser.find_elements(By.CLASS_NAME, 'item-title')
		item_descriptions = self.browser.find_elements(By.CSS_SELECTOR, 'p.description')
		return zip(menu_items, item_descriptions)

		#select menu items by css selector (class): item-title
		#select menu item description by css selector: p.description
		#zip the two lists together into a dict and RETURN list of tuples

	def closeBrowser(self):
		if self.browser:
			self.browser.quit()

restuarant_name = 'House of Curries'
restuarant_addr = '2520 Durant Ave, Berkeley, CA, 94704'
scraper = Scraper(restuarant_name, restuarant_addr)
scraper.startBrowser()
scraper.searchRestuarant()
scraper.selectRestaurantFromResults()
menu_dict = scraper.pairMenuItemsAndDescriptions()
scraper.closeBrowser()

print(restuarant_name)
print(restuarant_addr)
for k, v in menu_dict:
	print(k, v)
