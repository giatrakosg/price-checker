from bs4 import BeautifulSoup
import re
import requests
import shelve
import sys
import os
from urllib.parse import urlparse

# Item object stored in database
class Item(object):
    def __init__(self, price,title,size,url):
        self.price = price
        self.title = title
        self.size = size
        self.url = url
    def __str__(self):
        str =  self.title + " (" + repr(self.price) + ") "
        for x in self.size :
            str = str + " " + x
        return str
    # Equality function used by database for storing
    def __eq__(self,other):
        if (self.title == other.title):
            return True
        return False
    # We retrieve the website again and check for price changes .If there are we
    # we print a message
    def update(self):
    	target = requests.get(self.url)
    	soup = BeautifulSoup(target.text,"html.parser")
    	str = soup.find_all(itemprop='price')[0].contents[0]
    	price = getprice(str)
    	print(price)
    	if(price < self.price) :
            self.price = price
            print("New price on item " + self.title + "\nURL: " + self.url)

# Format the string correctly
def getprice(x):
    str = re.sub("[^0-9,.]", "", x)
    str = str.replace(',','.')
    price = float(str)
    return price
# Remove leading and trailing whitespace
def gettitle(x):
	str = x.strip()
	return str

# We open the shelve database
# see : https://docs.python.org/3.1/library/shelve.html
db = shelve.open('items.db')
# Print all the items in the database
if(str(sys.argv[1]) == 'show') :
	for x in db.keys():
		print(db[x])
# add new item in database.The url is given by the user
elif (str(sys.argv[1]) == 'add') :
    target_url = input("Please enter url:")
    # Returns a requests object
    target = requests.get(target_url)
    parsed_uri = urlparse(target_url)
    result = '{uri.scheme}://{uri.netloc}/'.format(uri=parsed_uri)
    print(result)

    # BeautifulSoup object used for scraping and finding elements
    soup = BeautifulSoup(target.text,"html.parser")
    # We extract the price (in the website we want it is in the itemprop tag)
    str = soup.find_all(itemprop='price')[0].contents[0]
    # We extract the title of the item .Has leading whitespace
    title = soup.find_all('div',{"class",'product-left__name-second'})[0].contents[0]
    price = getprice(str) # Formating
    title = gettitle(title) # Formating
    print(price)
    print(title)
    item = Item(price,title,['44'],target_url)
    db[title] = item
# If the user calls with delete all we remove entire db
elif (str(sys.argv[1]) == 'delete') :
	if(str(sys.argv[2]) == 'all') :
		os.remove('items.db')
    # Else we remove only the item by title given
	else :
		title = str(sys.argv[2])
		try :
			del db[title]
		except KeyError :
			print('Key not found')
# We cycle through the database and update all items
elif (str(sys.argv[1]) == 'update') :
	for x in db.keys():
		db[x].update()
elif (str(sys.argv[1]) == 'save') :
    target_url = input("Please enter url:")
    # Returns a requests object
    target = requests.get(target_url)
    #print(target.text)
    f = open('example.html','w+')
    f.write(target.text)
    f.close()

db.close()
