import urllib.request
from bs4 import BeautifulSoup


class ArticleInfo:

  def __init__(self, title, url):
    self.title = title
    self.url = url
    self.intro = ""

  def __str__(self):
    return "Title = " + self.title + "\n" + "Url = " + self.url + "\nIntro = " + self.intro

  def setIntro(self, intro):
    self.intro = intro

  def getIntro(self):

    with urllib.request.urlopen(self.url) as page:
      html = page.read()

    soup = BeautifulSoup(html, "html.parser")
    intro = soup.find("p", attrs={"class":"article-summary"})
    if(intro):
      self.intro = intro.get_text()