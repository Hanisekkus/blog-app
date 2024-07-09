from pathlib import Path
from django.test import TestCase
from django.core.files.uploadedfile import SimpleUploadedFile

from blog.models import Tag, Article

TEST_DIR = Path(__file__).resolve().parent


class TagTestCase(TestCase):
    def test_tag_str(self):
        tag = Tag(name='Tag1')
        self.assertEqual(str(tag), 'Tag1')


class ArticleTestCase(TestCase):
    def test_article_str(self):
        article = Article(title='Article 1', content='Content 1', image=SimpleUploadedFile('image.png', open(TEST_DIR / 'images'/ 'image.png', 'rb').read(), content_type='image/png'))
        self.assertEqual(str(article), 'Article 1')
