# git-checker
 A utility that check prices for certain sites

## Sites suported
 1. epapoutsia.gr
 2. mrporter.com

## Install
    $pip install pipenv
    $pipenv install
## Usage

Show all items in the database  

    $python main.py show  

Add item from url to database  

    $python add  

Delete all items from database  

    $python delete all  

Delete item with title from database  

    $python delete [title]  

Retrieves prices from sites and shows if there are any drops

    $python update  
