from django.test import TestCase
from django.urls import resolve, reverse
from ..models import Forum
from ..views import home

class HomeTests(TestCase):
    def setUp(self):
        self.forum = Forum.objects.create(name='Django', description='This is Django Forum')
        url = reverse('home')
        self.response = self.client.get(url)

    def test_home_view_status_code(self):
        # testing status code of the response for homepage
        # The status code 200 means success.
        self.assertEquals(self.response.status_code, 200)
    
    def test_home_url_resolves_home_view(self):
        # test for the correct view function for the requested homepage URL
        view = resolve('/webforum/')
        self.assertEquals(view.func, home)

    def test_home_view_contains_link_to_topics_page(self):
        forum_topics_url = reverse('forum_topics', kwargs={'pk': self.forum.pk})
        self.assertContains(self.response, 'href="{0}"'.format(forum_topics_url))
