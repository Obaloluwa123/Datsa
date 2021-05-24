import requests
from django.shortcuts import render
from bs4 import BeautifulSoup
# Create your views here.
def home(request):
    return render(request, 'base.html')

def search(request):
    search = request.POST.get('search')
    print(search)

    frontend = {
        'search': search
    }
    return render(request, 'app/search.html', frontend)
