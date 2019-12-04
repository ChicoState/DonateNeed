from django.http import HttpRequest
from django.test import SimpleTestCase
from django.test import TestCase
from django.urls import reverse
from myapp.views import *
#from myapp.models import Agencies
#from .forms import *

class sanity_test(SimpleTestCase):
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
