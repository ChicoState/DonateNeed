from django.shortcuts import render
from django.shortcuts import redirect


# Create your views here.
def home(request):
    class Card:
      def __init__(self, name, url, picUrl, address, phone):
        self.name = name
        self.url = url
        self.picUrl = picUrl
        self.address = address
        self.phone = phone

    newCard = [
      Card("American Red Cross", "https://www.redcross.org", "media/redCross.jpg", "2125 East Onstott Road Yuba City, CA 95991","(530) 673-1460"),
      Card("Neighborhood Church of Chico", "http://www.ncchico.org/", "media/NC.jpg", "2801 Notre Dame Boulevard Chico, CA 95928", "(530) 343-6006"),
      Card("Northern Valley Catholic Social Service", "https://www.redcross.org", "media/NVCSS.png", "2400 Washington Ave Redding, CA 96001-2832", "(530) 345-1600")
    ]

    context = {
      "cards": newCard,
      "ranger": range(0, 3),
    }
    
    return render(request, 'main/index.html', context=context)


def agencies(request):
    class Card:
      def __init__(self, name, url, picUrl, address, phone):
        self.name = name
        self.url = url
        self.picUrl = picUrl
        self.address = address
        self.phone = phone

    newCard = [
      Card("Red Cross", "https://www.redcross.org", "media/redCross.jpg", "2125 East Onstott Road Yuba City, CA 95991","(530) 673-1460"),
      Card("Neighborhood Church of Chico", "http://www.ncchico.org/", "media/NC.jpg", "2801 Notre Dame Boulevard Chico, CA 95928", "(530) 343-6006"),
      Card("Northern Valley Catholic Social Service", "https://www.redcross.org", "media/NVCSS.png", "2400 Washington Ave Redding, CA 96001-2832", "(530) 345-1600")
    ]
    context = {
      "cards": newCard,
      "ranger": range(0, 3),
    }
    

    return render(request, 'main/agencies.html', context=context)


def trending(request):
    context = {
    }
    
    return render(request, 'main/trending.html', context=context)

def about(request):
   return render(request, 'main/about.html', context = {})