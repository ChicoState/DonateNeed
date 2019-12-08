from django.http import HttpRequest
from django.test import SimpleTestCase
from django.test import TestCase
from django.urls import reverse
from myapp.views import *
from myapp.models import *
from myapp.forms import RegistrationForm

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

   # def test_model_News_Articles(self):
       # test = News_Articles.objects.get(id=1)
       # pic = test.picture
       # self.assertEquals(pic,'media/redCross.jpg')

class form_test(TestCase):
    def test_form(self):
        form = RegistrationForm()
        self.assertEquals(form.fields['password1'].label, 'Password' )
        self.assertEquals(True,True)

