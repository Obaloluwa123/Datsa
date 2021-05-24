import requests
from requests.compat import quote_plus
from django.shortcuts import render
from . import models
from bs4 import BeautifulSoup

BASE_CRAIG_URL = 'https://losangeles.craigslist.org/search/?query={}'
BASE_IMAGE_URLS = 'https://images.craigslist.org/{}_300x300.jpg'
# Create your views here.


def home(request):
    return render(request, 'base.html')

def search(request):
    search = request.POST.get('search')
    models.Search.objects.create(search=search)

    final_url = BASE_CRAIG_URL.format(quote_plus(search))
    response = requests.get(final_url)
    data = response.text
    soup = BeautifulSoup(data, features='html.parser')

    post_listings = soup.find_all('li', {'class': 'result-row'})


    live_posting = []
    for posts in post_listings:
        post_title = posts.find(class_='result-title').text
        post_url = posts.find('a').get('href')
        if posts.find(class_='result-price'):
            post_price = posts.find(class_='result-price').text
        else:
            post_price = 'N/A'
        if posts.find(class_='result-image').get('data-ids'):
            post_images_id = posts.find(class_='result-image').get('data-ids').split(',')[0].split(":")[1]
            post_images_url = BASE_IMAGE_URLS.format(post_images_id)
            print(post_images_url)
        else:
            post_images_url = 'https://craigslist.org/images/peace.jpg'
        live_posting.append((post_title, post_url, post_price, post_images_url))


    frontend = {
        'search': search,
        'live_posting': live_posting,
    }
    return render(request, 'app/search.html', frontend)
