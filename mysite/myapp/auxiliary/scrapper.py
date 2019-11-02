# import libraries
import urllib.request
from bs4 import BeautifulSoup
import sys
sys.path.append("../")

import models


class articleInfo:

  def __init__(self, title, url):
    self.title = title
    self.url = url
    self.intro = ""

  def __str__(self):
    return "Title = " + self.title + "\n" + "Url = " + self.url + "\nIntro = " + self.intro

  def setIntro(self, intro):
    self.intro = intro




def getIntro(url, article):

  with urllib.request.urlopen(url) as page:
    html = page.read()

  soup = BeautifulSoup(html, "html.parser")
  intro = soup.find("p", attrs={"class":"article-summary"})
  if(intro):
    article.intro = intro.get_text()

# specifiy the url
quote_page = 'https://www.actionnewsnow.com/'

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

articles = []

#
for article in newsArticles:

  for child in article:
    articles.append(articleInfo(child.get_text(), child.get('href')))
    getIntro(articles[-1].url, articles[-1])

    print(articles[-1])

  print("-------------------------------------------")


