from bs4 import BeautifulSoup
import shelve


db = shelve.open("items.db")

with open("example.html") as fp :
    soup = BeautifulSoup(fp,"html.parser")

print(soup.title)
print(soup.find_all(itemprop='price')[0].contents[0])

db.close()
