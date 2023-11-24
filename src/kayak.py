import requests
import re
from bs4 import BeautifulSoup

headers = {'User-Agent' : 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36'}

def getBoatsFromColoradoKayak():
    boatlist = []
    url = 'https://coloradokayak.com/collections/whitewater-kayaks'

    r = requests.get(url, headers=headers)
    soup = BeautifulSoup(r.text, 'html.parser')
    mainboatarea = soup.find_all('div', {'class': 'card'})
    for pages in mainboatarea:
        header = pages.find('h1', {'class': 'heading'})
        # only shop all whitewater kayak is set up this way so we don't need more detailed statement
        if header:
            boats = pages.find_all('div', {'class': 'product-item'})
            for boat in boats:
                productUrl = url
                actionButton = boat.find('button', {'class': 'product-item__action-button'})
                imgElement = boat.find('img', {'class': 'product-item__primary-image'})

                if actionButton.has_attr('data-product-url'): 
                    productUrl = url + actionButton['data-product-url']

                boatObject = {
                    'website': 'Colorado Kayak',
                    'by-ref': 'colorado-kayak',
                    'title': boat.find('a', {'class': 'product-item__title'}).text,
                    'link': productUrl,
                    'price': re.sub("\D", "", boat.find('span', {'class': 'price'}).text),
                    'image': 'https:' + imgElement['data-src']
                }
                boatlist.append(boatObject)
    return boatlist

def getBoatsFromRutabaga():
    boatlist = []
    url = 'https://www.rutabagashop.com/collections/kayaks-whitewater'

    r = requests.get(url, headers=headers)
    soup = BeautifulSoup(r.text, 'html.parser')
    mainboats = soup.find_all('div', { 'class': 'product-item'})
    for boat in mainboats:
        starterUrl = 'https://www.rutabagashop.com/'
        brand = boat.find('a', {'class': 'product-item__vendor'}).text
        boatName = boat.find('a', {'class': 'product-item__title'}).text
        link = boat.find('a', {'class': 'product-item__image-wrapper'})['href']
        price =  re.sub("\D", "", boat.find('span', {'class': 'price'}).text)
        finalPrice = price[:-2]
        # image srcs aren't accessible
        boatObject = {
            'website': 'Rutabaga Shop',
            'by-ref': 'rutabaga-shop',
            'title': brand + ' ' + boatName,
            'link': starterUrl + link,
            'price': finalPrice
        }
        boatlist.append(boatObject)
    return boatlist

def getBoatsFromNextAdventure():
    boatlist = []
    for x in range(0, 2):
        url = 'https://www.nextadventure.net/shop/paddle/kayaks/whitewater-kayaks?p={page}'

        r = requests.get(url, headers=headers)
        soup = BeautifulSoup(r.text, 'html.parser')
        boats = soup.find_all('div', {'class': 'product-item-info'})

        for item in boats:
            img = item.find('img', {'class': 'product-image-photo'})
            boat = {
            'website': 'Next Adventure',
            'by_ref': 'next-adventure',
            'title': item.find('a', {'class': 'product-item-link'}).text,
            'link': item.find('a', {'class': 'product-item-link'})['href'],
            'price': item.find('div', {'class': 'price-final_price'}).text if item.find('div', {'class': 'price-final_price'}) else '',
            'image': img['data-src'] if img['data-src'] else img['src'] 
            }
            boatlist.append(boat)
    return boatlist


def getAllKayaks():
    finalBoatList = []
    rutabaga = getBoatsFromRutabaga()
    coloradoKayaks = getBoatsFromColoradoKayak()
    nextAdventure = getBoatsFromNextAdventure()

    finalBoatList.append(rutabaga)
    finalBoatList.append(coloradoKayaks)
    finalBoatList.append(nextAdventure)

    return finalBoatList
