from django.db import models
from django.db.models import PROTECT
from django.core.exceptions import ValidationError
from django.core.validators import MaxValueValidator, MinValueValidator
from django.contrib.auth.models import User
class Color(models.Model):

    class Meta:
        verbose_name_plural = 'цвета'
        verbose_name = 'цвет'

    name = models.CharField(verbose_name='цвет', max_length=100)

    def __str__(self):
        return self.name

class Size(models.Model):

    class Meta:
        verbose_name_plural = 'размеры'
        verbose_name = 'размер'

    name = models.CharField(verbose_name='размер', max_length=100)

    def __str__(self):
        return self.name


class Advertising(models.Model):

    class Meta:
        verbose_name_plural = 'рекламы'
        verbose_name = 'реклама'

    name = models.CharField(verbose_name='название', max_length=100)
    image = models.ImageField(verbose_name='фото', upload_to='images_advertising/')

    def __str__(self):
        return self.name


class Type(models.Model):

    class Meta:
        verbose_name_plural = 'типы'
        verbose_name = 'тип'

    name = models.CharField(verbose_name='название', max_length=100)


    def __str__(self):
        return self.name

class Category(models.Model):

    class Meta:
        verbose_name_plural = 'категории'
        verbose_name = 'категория'

    name = models.CharField(verbose_name='название', max_length=100)

    def __str__(self):
        return self.name


class Review(models.Model):
    product = models.ForeignKey('market.Product', on_delete=models.PROTECT, related_name='reviews')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.PositiveIntegerField(choices=[(i, f"{i} Stars") for i in range(1, 6)])
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Review by {self.user} for {self.product.name}"


class ProductRating(models.Model):
    product = models.ForeignKey('market.Product', on_delete=models.CASCADE, related_name='ratings')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.PositiveIntegerField(choices=[(i, f"{i} Stars") for i in range(1, 6)])

    class Meta:
        unique_together = ('product', 'user')


class Product(models.Model):

    class Meta:
        verbose_name_plural = 'товары'
        verbose_name = 'товар'

    name = models.CharField(verbose_name='название', max_length=100)
    description = models.TextField(verbose_name='описание')
    color = models.ManyToManyField('market.Color', verbose_name='выберите цвета', related_name='product')
    size = models.ManyToManyField('market.Size', verbose_name='выберите размер', blank=True, null=True)
    image = models.ImageField(verbose_name='фото', upload_to='images_products/')
    image1 = models.ImageField(verbose_name='фото1', upload_to='images_products/', blank=True, null=True)
    image2 = models.ImageField(verbose_name='фото2', upload_to='images_products/', blank=True, null=True)
    image3 = models.ImageField(verbose_name='фото3', upload_to='images_products/', blank=True, null=True)
    image4 = models.ImageField(verbose_name='фото4', upload_to='images_products/', blank=True, null=True)
    price = models.DecimalField(verbose_name='цена', max_digits=10, decimal_places=2)
    category = models.ForeignKey('market.Category', on_delete=PROTECT, related_name='product')
    types = models.ForeignKey('market.Type', on_delete=PROTECT, related_name='product', blank=True, null=True)
    old_price = models.DecimalField(verbose_name='цена', max_digits=10, decimal_places=2, blank=True, null=True)
    view = models.PositiveIntegerField(verbose_name='просмотры', default=0, validators=[MinValueValidator(0)])
    rating = models.IntegerField(default=0, choices=[(i, f"{i} Stars") for i in range(1, 6)])
    author = models.ForeignKey('auth.User', on_delete=models.CASCADE, related_name='news', verbose_name='автор',
                                   null=True)
    total_rating = models.PositiveIntegerField(default=0)
    total_reviews = models.PositiveIntegerField(default=0)
    date = models.DateTimeField(verbose_name='date', auto_now_add=True)



    def __str__(self):
        return self.name

    def get_average_rating(self):
            reviews = self.reviews.all()
            if reviews.exists():
                return sum([review.rating for review in reviews]) / reviews.count()
            return 0

# Create your models here.
