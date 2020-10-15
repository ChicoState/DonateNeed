# import libraries
import os
import django
from django.core.files import File
os.environ["DJANGO_SETTINGS_MODULE"] = 'mysite.settings'
django.setup()
from myapp import models
import cssutils

import urllib.request
from urllib.request import urlopen
import time
from bs4 import BeautifulSoup
i = 1

def getIntro(url):

  with urllib.request.urlopen(url) as page:
    html = page.read()

  soup = BeautifulSoup(html, "html.parser")
  intro = soup.find("h2", attrs={"class":"Heading__HeadingStyled-sc-1w5xk2o-0-h2 eFMthj Heading-sc-1w5xk2o-1 HeroArticle__ArticleDeck-sc-1gllxr3-0 juNLjK"})
  if(intro):
    return intro.get_text()


def getPicture(url):

  with urllib.request.urlopen(url) as page:
    html = page.read()

  soup = BeautifulSoup(html, "html.parser")
  picture = soup.find("figure")




  #print(picture)
  selectors = {}

  #picture = soup.find("div", attrs={"class":"BackdropImage-container-2S9Qf"})
  if(picture):
      picture = picture.prettify()
     # print(picture)

      # picture = soup.find_all("div", {'class': lambda s: 'BackdropImage' in s})
      # print(picture)
      #print(picture.select('style'))
      #
      # for styles in picture.select('style'):
      #
      #     print(styles)
      #     css = cssutils.parseString(styles.encode_contents())
      #     for rule in css:
      #         if rule.type == rule.STYLE_RULE:
      #             style = rule.selectorText
      #             selectors[style] = {}
      #             for item in rule.style:
      #                 propertyname = item.name
      #                 value = item.value
      #                 selectors[style][propertyname] = value
      #                 print(value)
      #pic = picture.find("div", attrs={"class": "BackdropImage-container-2S9Qf"})
      #pic = picture.find_all("div")
      #print(pic)
      # if(picture['src'] == 'https://ftp2.actionnewsnow.com/Watches%20and%20Warnings.jpg'):
      #     # picture['src'] = 'https://www.realmilkpaint.com/wp-content/uploads/SoftWhite_Edited_2018.jpg'
      #     return None
      # return picture['src']
      return picture


while(1):
  print("Starting Up")


  j = str(i)
  print(j)
  # specifiy the url
  #quote_page = 'https://www.actionnewsnow.com/news/local/'

  quote_page = 'https://www.reuters.com/news/archive/tsunami?view=page&page=' + j


  #query the website and return the html to the variable 'page'
  #html = urlopen(quote_page, timeout=10).read()
  with urllib.request.urlopen(quote_page, timeout=10) as page:
      html = page.read()

  # parse the html using BeautifulSoup
  soup = BeautifulSoup(html, "html.parser")
  betterSoup = soup.prettify()

  # Find individual newsArticles
  #newsArticles = soup.find_all("h2", attrs={"class": "entry-title"})
  soup2 = soup.find("div", attrs={"class": "column1 col col-10"})

  newsArticles = soup2.find_all("article", attrs={"class": "story"})

  # Scrape topNews
  images = soup.find_all("a")
  results = open('record.txt', 'w')

  #
  for article in newsArticles:

    url = 'https://www.reuters.com'+(article.find('a').get('href'))
    if models.News_Articles.objects.filter(url = url).count() == 0:

        art = models.News_Articles(url=quote_page+(article.find('a').get('href')), title=article.find('a').get_text())

        title = article.find('h3', attrs={"class": "story-title"})
        title = title.text
        title = title.lstrip()

        url = 'https://www.reuters.com'+(article.find('a').get('href'))
        art.url = url

        art.title = title
        description = article.find('p').text
        art.description = description



        image = article.find('img').get('org-src')
        art.picture = image
        art.save()

        print("[", art.id, "]", art.title)

  print("-------------------------------------------")

  print("Resting")

  i = i+1
  time.sleep(5)
