from bs4 import BeautifulSoup
import shelve

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



db = shelve.open("items.db")

with open("example.html") as fp :
    soup = BeautifulSoup(fp,"html.parser")

item_title = input("Enter item title : ")

#print(soup.title)
str = soup.find_all(itemprop='price')[0].contents[0]
str = str.replace('€','')
str = str.replace(' ','')
str = str.replace(',','.')
price = float(str)

m = Item(price,item_title,['M','S'],'https://www.factoryoutlet.gr/gr-el/online-shop/andrika/royxa/poykamisa/1534507.0_0106-scotch-&-soda')
cunt = Item(6.3,item_title,['M','S'],'https://www.factoryoutlet.gr/gr-el/online-shop/andrika/royxa/poykamisa/1534507.0_0106-scotch-&-soda')
db[item_title] = m
db[item_title] = cunt


for x in db.keys() :
    print(db[x])

db.close()
