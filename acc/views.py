from django.shortcuts import render
from django.views import View
from django.conf import settings
import requests
from .models import Profile
from django.contrib.auth.models import User
import json
from django.contrib.auth import login, logout
import pdb
from django.http import HttpResponseRedirect, Http404
from bs4 import BeautifulSoup
import urllib
from .models import Product

# Create your views here.


class handleCode(View):

    def get(self,request, *args, **kwargs):
        access_token=request.GET.get('access_token')
        url='https://steemconnect.com/api/oauth2/token'
        me_url='https://steemconnect.com/api/me'
        #data={'code':code, 'client_secret':settings.CLIENT_SECRET}
        #response=requests.post(url, data=data)
        #response=response.json()
        #username=response.get('username')
        #refresh_token=response.get('refresh_token')
        #access_token=response.get('access_token')
        headers={'Authorization': access_token}
        me_response=requests.get(me_url,headers=headers)
        me_response=me_response.json()
        #pdb.set_trace()
        username=me_response.get('account').get('name')
        posting_key=me_response.get('account').get('posting').get('key_auths')[0][0]
        active_key=me_response.get('account').get('active').get('key_auths')[0][0]
        memo_key=me_response.get('account').get('memo_key')

        try:
            user=User.objects.get(username=username)
            profile=Profile.objects.get(user=user)
            #profile.refresh_token=refresh_token
            profile.access_token=access_token
            profile.save()
        except User.DoesNotExist:
            user=User.objects.create_user(username=username)
            profile=Profile.objects.create(posting_key=posting_key, active_key=active_key,
                                           memo_key=memo_key, user=user, access_token=access_token)
        user=login(request, user)
        request.session['access_token'] = access_token
        return HttpResponseRedirect('/')


        #request.session['access_token']=response.get('access_token')
        #pdb.set_trace()

        #sportherald.pythonanywhere.com


def user_logout(request):
    if request.user.is_authenticated:
        logout(request)
        return HttpResponseRedirect('/')
    else:
        return Http404('Invalid url')





def search_cap_us(query='brush'):
    products = []
    header = {'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.9; rv:32.0) Gecko/20100101 Firefox/32.0', }
    params = urllib.parse.urlencode({"search_query": query})
    search_url='http://shop.cap-us.com/search.php'
    response = requests.get(search_url, params, headers=header)
    soup = BeautifulSoup(response.content, "html.parser")
    product_lists = soup.find_all("li", class_="ListView")
    for item in product_lists:

        p = Product()
        div = item.find_all("div", class_="ProductImage")

        a = div[0].find_all("a")
        p.image_url = a[0].img["src"]
        p.manufacturer_url = a[0]["href"]
        #pdb.set_trace()
        detail_div = item.find_all("div", class_="ProductDetails")
        #pdb.set_trace()
        title_a = detail_div[0].find_all("a")
        p.search_term=query
        description=item.find_all("p", class_="ProductDescription")
        #pdb.set_trace()
        p.details=description[0].text
        titleprice = title_a[0].text
        list_stuff=process_title(titleprice)
        p.title=list_stuff[0]
        p.price=list_stuff[1]
        p.save()


def process_title(titleprice):
    titlepricelist=titleprice.split('$')
    price=titlepricelist[1]
    titlepricelist[1]=float(price)
    #pdb.set_trace()
    return titlepricelist



def colparmer(query='brush'):
    scraped_products = []
    search_url='https://www.coleparmer.com/search'
    params = urllib.parse.urlencode({"searchterm": query})
    response = requests.get(search_url, params)
    soup = BeautifulSoup(response.content, "html.parser")

    products_div=soup.find_all("div", class_='eb-productListing')
    try:
        product_ul=products_div[0].find_all("ul", recursive=False)
    except:
        return scraped_products
    product_lists=product_ul[0].find_all("li", recursive=False)
    for product in product_lists:
        p = Product()
        title_div=product.find_all("div", class_='eb-productname')
        atitle=title_div[0].find_all("a")
        p.title=atitle[0].text
        p.manufacturer_url=atitle[0]["href"]
        img=product.find_all("img", class_="lazy")
        p.image_url=img[0]['data-original']
        #pdb.set_trace()
        #apiece=product.find_all("a", class_="btn-add-cart")
        #p.pieces=get_piece(apiece[0].text)
        price_range=product.find_all("span", class_="price-range")
        p.price=process_price(price_range[0])
        description=product.find_all("span", class_="spec-list-value-box")
        p.details='Product Type:'+ description[0].text
        scraped_products.append(p)
    return scraped_products



def get_piece(text):
    text_list=text.split(' ')
    return text_list[2]

def process_price(price_range):
    prices=price_range.text
    prices=prices.strip()
    prices_list=prices.split(' ')
    price=prices_list[0]
    price=price.replace('$','')
    price=float(price)
    return price

def diamonddental(query):
    scraped_products = []
    search_url = 'http://www.diamonddentalsupplies.com/search'
    params = urllib.parse.urlencode({"q": query})
    response=requests.get(search_url, params)
    soup=BeautifulSoup(response.content, "html.parser")
    product_list=soup.find_all("div", class_="product-item")
    for product in product_list:
        p=Product()
        p.title=product.h2.text
        imgdiv=product.find_all('div', class_='picture')
        imagea=imgdiv[0].a
        p.manufacturer_url=imagea['href']
        p.image_url=imagea.img['src']
        description=product.find_all('div' , class_='description')
        p.details=description[0].text
        price_con=product.find_all('span', class_='price')
        price=price_con[0].text
        price=price.strip()
        price_list=price.split(' ')
        if price_list[0] == 'From':
            price=price_list[1]
        else:
            price=price_list[0]
        price = price.replace('$', '')
        #pdb.set_trace()
        p.price=float(price)
        scraped_products.append(p)
    return scraped_products

def blowoutmedical(query='brush'):
    scraped_products = []
    search_url='https://www.blowoutmedical.com/catalogsearch/result/'
    params = urllib.parse.urlencode({"q": query})
    response = requests.get(search_url, params)
    soap=BeautifulSoup(response.content, 'html.parser')
    item_inners=soap.find_all('div', class_='item-inner')
    for product in item_inners:
        p=Product()
        imagea=product.find_all('a', class_="product-image")
        p.manufacturer_url=imagea[0]['href']
        p.image_url=imagea[0].img['src']
        p.title=imagea[0].img['alt']
        price=product.find_all('span', class_='price')[0]
        #pdb.set_trace()
        p.price=float(price.text.strip().replace('$', ''))
        scraped_products.append(p)
    return scraped_products



def iqdentalsupply(query='brush'):
    search_url='http://www.iqdentalsupply.com/Shop'
    base_url='http://www.iqdentalsupply.com'
    scraped_products=[]
    parmas=urllib.parse.urlencode({'search':query})
    response=requests.get(search_url, parmas)
    soup=BeautifulSoup(response.content, 'html.parser')
    product_lists=soup.find_all('div', class_='cell')
    for product in product_lists:
        p=Product()
        atag=product.find_all('a', class_='thumbnail')
        p.manufacturer_url=base_url+atag[0]['href']
        p.image_url=base_url+atag[0].img['src']
        p.title=product.h3.a.text
        try:
            tds=product.find_all('td', 'texttable')
            p.price=float(tds[1].text.strip().replace('$',''))#use the first price in the list
        except:
            price=product.find_all('div', class_='price')
            p.price=float(price[0].h3.text.strip().replace('$', ''))
        scraped_products.append(p)
    return



def hygine_direct(query='brush'):
    scraped_products=[]
    search_url='http://www.hygiene-direct.com/search.php'
    params=urllib.parse.urlencode({'search_query':query})
    response=requests.get(search_url, params)
    soup=BeautifulSoup(response.content, 'html.parser')
    product_lists=soup.find_all('li', class_='ListView')
    for product in product_lists:
        #thumbnail is not on d detail search
        p=Product()
        atag=product.find_all('a', class_='ProductLink')
        p.title=atag[0].text
        p.manufacturer_url=atag[0]['href']
        p.price=float(product.find_all('span', class_='ProductPrice')[0].text.strip().split('$').pop())
        scraped_products.append(p)
    return scraped_products



def mendasearch(query='brush'):
    search_url='http://menda.descoindustries.com/Search/%s' % query
    response=requests.get(search_url)
    soup=BeautifulSoup(response.content, 'html.parser')
    ul=soup.find_all('ul', class_='grid')
    product_lists=ul[0].find_all('li', recursive=False)




























