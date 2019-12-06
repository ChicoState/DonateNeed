# import libraries
import os
import django
from django.core.files import File
os.environ["DJANGO_SETTINGS_MODULE"] = 'mysite.settings'
django.setup()
from myapp import models 

import urllib.request
import time
from bs4 import BeautifulSoup


def getIntro(url):

  with urllib.request.urlopen(url) as page:
    html = page.read()

  soup = BeautifulSoup(html, "html.parser")
  intro = soup.find("p", attrs={"class":"article-summary"})
  if(intro):
    return intro.get_text()


def getPicture(url):

  with urllib.request.urlopen(url) as page:
    html = page.read()

  soup = BeautifulSoup(html, "html.parser")
  picture = soup.find("img", attrs={"class":"img-fluid"})
  if(picture):
    return picture['src']


while(1):
  print("Starting Up")

  # specifiy the url
  quote_page = 'https://www.actionnewsnow.com/news/local/'

  #query the website and return the html to the variable 'page'
  with urllib.request.urlopen(quote_page) as page:
    html = page.read()

  # parse the html using BeautifulSoup
  soup = BeautifulSoup(html, "html.parser")
  betterSoup = soup.prettify()

  # Find individual newsArticles
  newsArticles = soup.find_all("h2", attrs={"class": "entry-title"})

  # Scrape topNews
  images = soup.find_all("a")
  results = open('record.txt', 'w')

  #
  for article in newsArticles:

    art = models.News_Articles(url=article.find('a').get('href'), title=article.find('a').get_text())
    art.description = getIntro(art.url)

    art.picture = getPicture(art.url)
    art.save()

    print("[", art.id, "]", art.title)

    print("-------------------------------------------")

  print("Resting")
  time.sleep(60)


