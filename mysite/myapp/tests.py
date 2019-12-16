from django.http import HttpRequest
from django.test import SimpleTestCase
from django.test import TestCase
from django.urls import reverse
from myapp.views import *
from myapp.models import *
from myapp.forms import RegistrationForm
import datetime
from django.test import Client
class home_view_test(TestCase):
    def test_Sanity(self):
        self.assertEqual(True,True)
    def test_home_url(self):
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
        self.assertContains(response,'<h1 class="display-3 text-center ml3" style="color:white">Changing the World, one Donation at a Time</h1>')
    def test_not_on_home_page(self):
        response=self.client.get('/')
        self.assertNotContains(response, 'i should not exist')
class Agencies_view_test(TestCase):
    def test_agencies_url(self):
        response = self.client.get('/agencies')
        self.assertEquals(response.status_code, 200)
    def test_trending_url(self):
        response = self.client.get('/trending')
        self.assertEquals(response.status_code, 200)
    def test_about_url(self):
        response = self.client.get('/about')
        self.assertEquals(response.status_code, 200)
    def test_Signup_url(self):
        response = self.client.post('/signUp')
        self.assertEquals(response.status_code, 200)
        
    def test_signin_url(self):
        response= self.client.get(reverse('login'))
        self.assertEquals(response.status_code, 200)

    def test_postsignin_url(self):
        response= self.client.get(reverse('postsignin'))
        self.assertEquals(response.status_code, 200)
    #def test_profile_url(self):
        #User.objects.create(username = 'batman', password = 'thisisrobin')
        #self.client.login(username='batman', password = 'thisisrobin')
        #response= self.client.post('/profile/batman')
        #self.assertEquals(response.status_code, 302)
    def test_agencySignUp_url(self):
        response= self.client.post(reverse('agencySignUp'))
        self.assertEquals(response.status_code, 200)
    #def test_agencyProfile(self):
        #response= self.client.get(reverse('agencyProfile'))
        #self.assertEquals(response.status_code, 200)

    def test_createProfile_url(self):
        user=User.objects.create(username = 'batman')
        user.set_password('thisisrobin')
        user.save()
        #self.client.login(username='batman', password = 'thisisrobin')
        c = Client()
        logged_in = c.login(username='batman', password='thisisrobin')
        response= self.client.post(reverse('createProfile'))
        self.assertTrue(logged_in)
        self.assertEquals(response.status_code, 302)
    def test_createcause_url(self):
        User.objects.create(username = 'batman', password = 'thisisrobin')
        self.client.login(username='batman', password = 'thisisrobin')
        response= self.client.post(reverse('createCause'))
        self.assertEquals(response.status_code, 302)
    def test_addAgency_url(self):
        User.objects.create(username = 'batman', password = 'thisisrobin')
        self.client.login(username='batman', password = 'thisisrobin')
        response= self.client.post(reverse('addAgency'))
        self.assertEquals(response.status_code, 302)

    def test_pledgesupport_url(self):
        user=User.objects.create(username = 'batman')
        user.set_password('thisisrobin')
        user.save()
        c = Client()
        logged_in = c.login(username='batman', password='thisisrobin')
        #login=self.client.login(username='batman', password = 'thisisrobin')
        response= self.client.post(reverse('pledgeSupport'))
        self.assertEquals(response.status_code, 302)
        self.assertTrue(logged_in)
    def test_agencyProfile(self):
        self.user=User.objects.create(username = 'batman', password = 'thisisrobin')
        login=self.client.login(username='batman', password = 'thisisrobin')
        response= self.client.post('/agencyProfile/batman')
        self.assertEquals(response.status_code, 302)
    def test_logoutview(self):
        response= self.client.post(reverse('logout'))
        self.assertEquals(response.status_code, 302)
    #def test_causepage(self):
        #self.user=User.objects.create(username = 'batman', password = 'thisisrobin')
        #login=self.client.login(username='batman', password = 'thisisrobin')
        #response= self.client.post('/causePage/batman')
        #self.assertEquals(response.status_code, 302)






class model_test(TestCase):
    def setUp(self):
        usher = User.objects.create(username = 'george')
        Agencies.objects.create(name = 'fred', email = 'test@gmail.com',address = '123 main st', url= 'google.com', phone = 5051234567 )
        News_Articles.objects.create(title='nothing',url = 'bing.com', description = 'Austin')
        Request_Fulfilled.objects.create(fulfilled_amount = '10', promised_amount = '11', promised_arrival = '2000-01-01')
        Request_In_Progress.objects.create(amount_total = '5',amount_fulfilled='2',is_complete=False,date_requested='2050-12-12',agency=Agencies.objects.get(id=1))
        #Account_Page.objects.create(requests_fulfilled=Request_Fulfilled.objects.get(id=1))
        #Agencies_Page.objects.create(causes='world domination', requests = Request_In_Progress.objects.get(id=1))
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
        self.assertEquals(True,True)

    def test_model_News_Articles(self):
        test = News_Articles.objects.get(id=1)
        self.assertEquals(test.url,'bing.com')

    def test_model_Request_Fulfilled(self):
        test = Request_Fulfilled.objects.get(id=1)
        famount=test.fulfilled_amount
        self.assertEquals(famount,10)
        pamount=test.promised_amount
        self.assertEquals(pamount,11)
        parrival=test.promised_arrival
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
        self.assertEquals(test.agency,Agencies.objects.get(id=1))

    def test_model_Account_Page(self):
        self.assertEquals(True,True)

    #def test_model_Agencies_Page(self):
        #test = Agencies_Page.objects.get(id=1)
        #self.assertEquals(test.causes,'world domination')
        #self.assertEquals(test.requests,Request_In_Progress.objects.get(id=1))

    def test_model_Causes(self):
        test = Cause.objects.get(id=1)
        self.assertEquals(test.title,'fancy feast')
        self.assertEquals(test.location, 'Hogwarts')




class form_test(TestCase):

    def test_RegistrationForm(self):
        valid_data = {
                "username": "test@gmail.com",
                "email": "test@yahoo.com",
                "password1": "s3cr3tshh",
                "password2": "s3cr3tshh",
                "first_name": "john",
                "last_name": "doe"
                }
        form = RegistrationForm(data=valid_data)
        self.assertEquals(form.fields['password1'].label, 'Password' )
        form.is_valid()
        self.assertFalse(form.errors)
    #def test_CauseForm(self):

