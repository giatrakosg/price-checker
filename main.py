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
db = shelve.open('items.db')
if(str(sys.argv[1]) == 'show') :
	for x in db.keys():
		print(db[x])
elif (str(sys.argv[1]) == 'add') :
	target_url = input("Please enter url:")
	target = requests.get(target_url)
	soup = BeautifulSoup(target.text,"html.parser")
	str = soup.find_all(itemprop='price')[0].contents[0]
	str = str.replace('€','')
	str = str.replace(' ','')
	str = str.replace(',','.')
	price = float(str)
	print(price)
elif (str(sys.argv[1]) == 'delete') :
	if(str(sys.argv[2]) == 'all') :
		os.remove('items.db')



db.close()
