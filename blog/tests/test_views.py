from pathlib import Path
from django.test import TestCase, Client
from django.urls import reverse
from django.core.cache import cache
from django.core.files.uploadedfile import SimpleUploadedFile

from blog.models import Article, Tag

TEST_DIR = Path(__file__).resolve().parent


class IndexViewTestCase(TestCase):
    def setUp(self):
        self.client = Client()

        # Create some test data
        self.tag1 = Tag.objects.create(name='tag1')
        self.tag2 = Tag.objects.create(name='tag2')
        self.article1 = Article.objects.create(title='Article 1', content='Content 1', image=SimpleUploadedFile('image.png', open(TEST_DIR / 'images'/ 'image.png', 'rb').read(), content_type='image/png'))
        self.article1.tags.add(self.tag1)
        self.article2 = Article.objects.create(title='Article 2', content='Content 2', image=SimpleUploadedFile('image.png', open(TEST_DIR / 'images'/ 'image.png', 'rb').read(), content_type='image/png'))
        self.article2.tags.add(self.tag2)
        self.article3 = Article.objects.create(title='Article 3', content='Content 3', image=SimpleUploadedFile('image.png', open(TEST_DIR / 'images'/ 'image.png', 'rb').read(), content_type='image/png'))
        self.article3.tags.add(self.tag1, self.tag2)

    def tearDown(self):
        # Clear cache after each test
        cache.clear()

    def test_view_is_available(self):
        # Test if the view is available
        response = self.client.get(reverse('blog:index'))
        self.assertEqual(response.status_code, 200)

    def test_no_query_or_tag(self):
        # Test when no query or tag is provided
        response = self.client.get(reverse('blog:index'))
        query_set = response.context['articles']
        self.assertEqual(query_set.count(), 3)
        self.assertQuerysetEqual(query_set, [self.article3, self.article2, self.article1])

    def test_query(self):
        # Test when a query is provided
        response = self.client.get(reverse('blog:index'), {'q': 'Article 1'})
        query_set = response.context['articles']
        self.assertEqual(query_set.count(), 1)
        self.assertQuerysetEqual(query_set, [self.article1])

    def test_tag(self):
        # Test when a tag is provided
        response = self.client.get(reverse('blog:index'), {'tag': 'tag1'})
        query_set = response.context['articles']
        self.assertEqual(query_set.count(), 2)
        self.assertQuerysetEqual(query_set, [self.article3, self.article1])

    def test_query_and_tag(self):
        # Test when both query and tag are provided
        response = self.client.get(reverse('blog:index'), {'q': 'Article', 'tag': 'tag2'})
        query_set = response.context['articles']
        self.assertEqual(query_set.count(), 2)
        self.assertQuerysetEqual(query_set, [self.article3, self.article2])
        

class ArticlesViewTestCase(TestCase):
    def setUp(self):
        self.client = Client()

        # Create some test data
        self.article1 = Article.objects.create(title='Article 1', content='Content 1', image=SimpleUploadedFile('image.png', open(TEST_DIR / 'images'/ 'image.png', 'rb').read(), content_type='image/png'))
        self.article2 = Article.objects.create(title='Article 2', content='Content 2', image=SimpleUploadedFile('image.png', open(TEST_DIR / 'images'/ 'image.png', 'rb').read(), content_type='image/png'))
        self.article3 = Article.objects.create(title='Article 3', content='Content 3', image=SimpleUploadedFile('image.png', open(TEST_DIR / 'images'/ 'image.png', 'rb').read(), content_type='image/png'))

    def tearDown(self):
        # Clear cache after each test
        cache.clear()

    def test_view_is_available(self):
        # Test if the view is available
        response = self.client.get(reverse('blog:articles'))
        self.assertEqual(response.status_code, 200)
    
    def test_view_pagination_is_available(self):
        # Test if the view is available
        response = self.client.get(f"{reverse('blog:articles')}?page=2")
        self.assertEqual(response.status_code, 200)

    def test_articles_list(self):
        # Test if the articles are listed correctly
        response = self.client.get(reverse('blog:articles'))
        query_set = response.context['articles']
        self.assertEqual(len(query_set), 2)
        self.assertListEqual(query_set, [self.article3, self.article2])

    def test_pagination(self):
        # Test if pagination is working correctly
        response = self.client.get(reverse('blog:articles'))
        self.assertContains(response, 'Article 3')
        self.assertContains(response, 'Article 2')
        self.assertNotContains(response, 'Article 1')

        response = self.client.get(f"{reverse('blog:articles')}?page=2")
        self.assertNotContains(response, 'Article 3')
        self.assertNotContains(response, 'Article 2')
        self.assertContains(response, 'Article 1')
