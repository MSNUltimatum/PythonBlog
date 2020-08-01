from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse
from PIL import Image

# Create your models here.

class News(models.Model):
    title = models.CharField('Название статьи', max_length=100, unique=True)
    text = models.TextField('Основной текст статьи')
    date = models.DateTimeField('Дата',default=timezone.now)
    avtor = models.ForeignKey(User, verbose_name='Автор', on_delete=models.CASCADE)
    img = models.ImageField('Фото к статье', default='bg_news.png', upload_to='news_images')

    views = models.IntegerField('Просмотры', default=1)
    # sizes = (
    #     ('S', 'Small'),
    #     ('M', 'Medium'),
    #     ('L', 'Large'),
    #     ('XL', 'Extra large')
    # )
    #
    # shop_sizes = models.CharField(max_length=2, choices=sizes,default='S')

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        super().save()
        image = Image.open(self.img.path)

        if image.height > 256 or image.width > 256:
            resize = (512, 512)
            image.thumbnail(resize)
            image.save(self.img.path)

    class Meta:
        verbose_name = 'Новость'
        verbose_name_plural = 'Новости'

    def get_absolute_url(self):
        return reverse('news-detail', kwargs={'pk' : self.pk})