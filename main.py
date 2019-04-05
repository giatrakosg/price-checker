from bs4 import BeautifulSoup
import requests
import shelve
import sys
import os 

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
    def __eq__(self,other):
        if (self.title == other.title):
            return True
        return False

def getprice(x):
	str = x.replace('€','')
	str = str.replace(' ','')
	str = str.replace(',','.')
	price = float(str)
	return price
def gettitle(x):
	str = x.strip()
	return str

db = shelve.open('items.db')
if(str(sys.argv[1]) == 'show') :
	for x in db.keys():
		print(db[x])
elif (str(sys.argv[1]) == 'add') :
	target_url = input("Please enter url:")
	target = requests.get(target_url)
	soup = BeautifulSoup(target.text,"html.parser")
	str = soup.find_all(itemprop='price')[0].contents[0]
	title = soup.find_all('div',{"class",'product-left__name-second'})[0].contents[0]
	price = getprice(str)
	title = gettitle(title)
	print(price)
	print(title)
	item = Item(price,title,['44'],target.text)
	db[title] = item
elif (str(sys.argv[1]) == 'delete') :
	if(str(sys.argv[2]) == 'all') :
		os.remove('items.db')
	else :
		title = str(sys.argv[2])
		try :
			del db[title]
		except KeyError :
			print('Key not found')


db.close()
