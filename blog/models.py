from PIL import Image
from io import BytesIO

from django.db import models
from django.core.files import File


class Tag(models.Model):
    name = models.CharField(max_length=20)
    
    def __str__(self) -> str:
        return self.name

class Article(models.Model):
    title = models.CharField(max_length=50)
    content = models.TextField(max_length=1000)
    image = models.ImageField()   
    thumb_image = models.ImageField(blank=True)
    tags = models.ManyToManyField(Tag, blank=True)

    # Default ordering for query methods
    class Meta:
        ordering = ['-id']

    def create_thumbnail(self) -> File | None:
        thumbnail_image: BytesIO = BytesIO()

        im: Image.Image = Image.open(self.image.file).copy()
        im.thumbnail((100, 100))
        im.save(thumbnail_image, 'PNG')
        im.close()
        
        return File(thumbnail_image, name=f'thumb_{self.image.name}')
    
    def save(self, *args, **kwargs):
        self.thumb_image = self.create_thumbnail()
        super().save(*args, **kwargs)

    def __str__(self) -> str:
        return self.title
