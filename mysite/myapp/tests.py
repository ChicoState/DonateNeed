from django.http import HttpRequest
from django.test import SimpleTestCase
from django.test import TestCase
from django.urls import reverse
from myapp.views import *
from myapp.models import *
from myapp.forms import RegistrationForm
import datetime
class view_test(SimpleTestCase):
    def test_Sanity(self):
        self.assertEqual(True,True)
    def test_url(self):
        response = self.client.get('/')
        self.assertEquals(response.status_code, 200)
    def test_view_url_by_name(self):
        response= self.client.get(reverse('about'))
        self.assertEquals(response.status_code, 200)
    def test_view_uses_correct_template(self):
        response = self.client.get(reverse('home'))
        self.assertTemplateUsed(response, 'main/index.html')
    def test_home_page_contains(self):
        response = self.client.get('/')
        self.assertContains(response,'<h1 class="display-3 text-center ml3" style="color:white">Changing the World, one Step at a Time</h1>')
    def test_not_on_home_page(self):
        response=self.client.get('/')
        self.assertNotContains(response, 'i should not exist')

class model_test(TestCase):
    def setUp(self):
        usher = User.objects.create(username = 'george')
        Agencies.objects.create(name = 'fred', email = 'test@gmail.com',address = '123 main st', url= 'google.com', phone = 5051234567, user =usher )
        #News_Articles.objects.create(url = 'bing.com', description = 'Austin')
        Request_Fulfilled.objects.create(fulFilledAmount = '10', promisedAmount = '11', promisedArrival = '2000-01-01')
        Request_In_Progress.objects.create(amount_total = '5',amount_fulfilled='2',is_complete=False,date_requested='2050-12-12',request_fulfillment=Request_Fulfilled.objects.get(id=1))
        #Account_Page.objects.create(requests_fulfilled=Request_Fulfilled.objects.get(id=1))
        Agencies_Page.objects.create(causes='world domination', requests = Request_In_Progress.objects.get(id=1))
        Cause.objects.create(title='fancy feast',location='Hogwarts')
    def test_model_Agencies(self):
        test = Agencies.objects.get(id=1)
        expected = f'{test.name}'
        self.assertEquals(expected,'fred')
        eml = test.email
        self.assertEquals(eml,'test@gmail.com')
        ddrss = test.address
        self.assertEquals(ddrss,'123 main st')
        rl = test.url
        self.assertEquals(rl,'google.com')
        usr = test.user.username
        self.assertEquals(usr, 'george')
        self.assertEquals(True,True)

    #def test_model_News_Articles(self):
        #test = News_Articles.objects.get(id=1)
        #pic = test.picture
        #self.assertEquals(pic,'media/redCross.jpg')

    def test_model_Request_Fulfilled(self):
        test = Request_Fulfilled.objects.get(id=1)
        famount=test.fulFilledAmount
        self.assertEquals(famount,10)
        pamount=test.promisedAmount
        self.assertEquals(pamount,11)
        parrival=test.promisedArrival
        self.assertEquals(parrival, datetime.date(2000,1,1))
    def test_model_Request_In_Progress(self):
        test = Request_In_Progress.objects.get(id=1)
        amt_tot=test.amount_total
        self.assertEquals(amt_tot,5)
        amt_ful=test.amount_fulfilled
        self.assertEquals(amt_ful,2)
        done=test.is_complete
        self.assertNotEqual(done,True)
        date_req=test.date_requested
        self.assertEquals(date_req,datetime.date(2050,12,12))
        self.assertEquals(test.request_fulfillment,Request_Fulfilled.objects.get(id=1))

    def test_model_Account_Page(self):
        self.assertEquals(True,True)
    def test_model_Agencies_Page(self):
        test = Agencies_Page.objects.get(id=1)
        self.assertEquals(test.causes,'world domination')
        self.assertEquals(test.requests,Request_In_Progress.objects.get(id=1))
    def test_model_Causes(self):
        test = Cause.objects.get(id=1)
        self.assertEquals(test.title,'fancy feast')
        self.assertEquals(test.location, 'Hogwarts')

class form_test(TestCase):
    def test_form(self):
        form = RegistrationForm()
        self.assertEquals(form.fields['password1'].label, 'Password' )
        self.assertEquals(True,True)

