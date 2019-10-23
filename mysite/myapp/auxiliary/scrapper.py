# import libraries
import urllib.request
import time
from bs4 import BeautifulSoup
from articleInfo import ArticleInfo


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

  articles = []

  #
  for article in newsArticles:
    articles.append(ArticleInfo(article.find('a').get_text(), article.find('a').get('href')))
    articles[-1].getIntro()

    print("", articles[-1])

    print("-------------------------------------------")

  print("Resting")
  time.sleep(60)

