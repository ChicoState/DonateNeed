from django.shortcuts import render
from django.shortcuts import redirect
import pyrebase

config = {
    'apiKey': "AIzaSyDGPibcqcm-BDI-yckPYFcXpPCFvhnPd3E",
    'authDomain': "donate-need.firebaseapp.com",
    'databaseURL': "https://donate-need.firebaseio.com",
    'projectId': "donate-need",
    'storageBucket': "donate-need.appspot.com",
    'messagingSenderId': "72050043145",
    'appId': "1:72050043145:web:28ef2b2e6ff1c08bdb4bd8",
    'measurementId': "G-ZM4B6MFKWJ"
}
firebase = pyrebase.initialize_app(config)
db=firebase.database()
auth = firebase.auth()


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
      Card("Red Cross", "https://www.redcross.org", "media/redCross.jpg", "2125 East Onstott Road Yuba City, CA 95991","(530) 673-1460"),
      Card("Neighborhood Church of Chico", "http://www.ncchico.org/", "media/NC.jpg", "2801 Notre Dame Boulevard Chico, CA 95928", "(530) 343-6006"),
      Card("Northern Valley Catholic Social Service", "https://www.redcross.org", "media/NVCSS.png", "2400 Washington Ave Redding, CA 96001-2832", "(530) 345-1600")
    ]

    class Article:
      def __init__(self, url, title, picUrl, summary):
        self.url = url
        self.title = title
        self.picUrl = picUrl
        self.summary = summary
    newArticle = [
      Article("https://www.cnbc.com/2019/05/16/six-months-after-camp-fire-survivors-struggle-to-find-temporary-homes.html", "Six months after California’s Camp Fire, survivors still struggle to find temporary homes", "static/media/fire.jpg", "The blaze in Northern California’s Butte County killed 86 people, destroyed about 14,000 homes and left most of the town of Paradise in ruins. It ranks as the deadliest and most destructive fire in California history."),
      Article("https://www.cnbc.com/2019/05/16/six-months-after-camp-fire-survivors-struggle-to-find-temporary-homes.html", "Hurricane Dorian Damage in Bahamas Explained", "static/media/fire.jpg", "Meteorologist Kait Parker says the damage in the Bahamas was caused by a combination of storm surge and winds.")
    ]
    context = {
      "cards": newCard,
      "articles": newArticle,
      "ranger": range(0, 5),
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
    class Article:
      def __init__(self, url, title, picUrl, summary):
        self.url = url
        self.title = title
        self.picUrl = picUrl
        self.summary = summary
    newArticle = [
      Article("https://www.cnbc.com/2019/05/16/six-months-after-camp-fire-survivors-struggle-to-find-temporary-homes.html", "Six months after California’s Camp Fire, survivors still struggle to find temporary homes", "static/media/fire.jpg", "The blaze in Northern California’s Butte County killed 86 people, destroyed about 14,000 homes and left most of the town of Paradise in ruins. It ranks as the deadliest and most destructive fire in California history."),
      Article("https://www.cnbc.com/2019/05/16/six-months-after-camp-fire-survivors-struggle-to-find-temporary-homes.html", "Hurricane Dorian Damage in Bahamas Explained", "static/media/fire.jpg", "Meteorologist Kait Parker says the damage in the Bahamas was caused by a combination of storm surge and winds.")
    ]
    context = {
      "articles": newArticle,
      "ranger": range(0, 5),
    }
    return render(request, 'main/trending.html', context=context)

def about(request):
   return render(request, 'main/about.html', context = {})

def signIn(request):
    return render(request, "main/signIn.html")

def postsign(request):
    email = request.POST.get('email')
    passw = request.POST.get("pass")
    try:
        user = auth.sign_in_with_email_and_password(email,passw)
    except:
        message = "invalid credentials"
        return render(request, "main/signIn.html", {"msg":message})
    print(user['idToken'])
    session_id=user['idToken']
    #get.session['uid']=str(session_id)
    return render(request, "main/welcome.html", {"e":email})

def logout(request):
    auth.logout(request)
    return render(request, 'signIn.html')

def SignUp(request):
    return render(request,"SignUp.html")

def SignUp(request):
    return render(request, "main/SignUp.html")

def postsignup(request):
    email = request.POST.get('email')
    passw = request.POST.get("pass")
    try:
        user = auth.create_user_with_email_and_password(email,passw)
    except:
        message = "bad signup"
        return render(request, "main/welcome.html", {"e":email})
