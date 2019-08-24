from django.test import TestCase
from django.urls import reverse, resolve
from .views import home

class HomeTests(TestCase):
    def test_home_view_status_code(self):
        # testing status code of the response for homepage
        url = reverse('home')
        response = self.client.get(url) 
        # The status code 200 means success.
        self.assertEquals(response.status_code, 200)
    
    def test_home_url_resolves_home_view(self):
        # test for the correct view function for the requested home URL
        view = resolve('/webforum/')
        self.assertEquals(view.func, home)


