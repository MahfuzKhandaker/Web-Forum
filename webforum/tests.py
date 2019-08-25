from django.test import TestCase
from django.urls import reverse, resolve
from .views import home, forum_topics
from .models import Forum

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
        # test for the correct view function for the requested URL
        view = resolve('/webforum/')
        self.assertEquals(view.func, home)

    def test_home_view_contains_link_to_topics_page(self):
        forum_topics_url = reverse('forum_topics', kwargs={'pk': self.forum.pk})
        self.assertContains(self.response, 'href="{0}"'.format(forum_topics_url))


class ForumTopicsTests(TestCase):
    def setUp(self):
        Forum.objects.create(name='Django', description='This is Django Forum')
    
    def test_forum_topics_view_status_code(self):
        url = reverse('forum_topics', kwargs={'pk':1})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_forum_topics_view_not_found_status_code(self):
        url = reverse('forum_topics', kwargs={'pk':11})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_forum_topics_url_resolves_forum_topics_view(self):
        view = resolve('/webforum/forums/1/')
        self.assertEqual(view.func, forum_topics)

    def test_forum_topics_view_contains_link_back_to_homepage(self):
        forum_topics_url = reverse('forum_topics', kwargs={'pk':1})
        response = self.client.get(forum_topics_url)
        home_page_url = reverse('home')
        self.assertContains(response, 'href="{0}"'.format(home_page_url))




