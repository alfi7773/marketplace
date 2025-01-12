from importlib.metadata import requires

from django import forms

from market.models import *
from django.db.models.fields import DecimalField



class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ('name', 'description', 'color', 'size', 'image', 'price', 'category', 'rating',)



    widgets = {
        'name': forms.TextInput(attrs={'class': 'create'}),
        'image': forms.ClearableFileInput(attrs={'class': 'width-file'}),
        'description': forms.Textarea(attrs={'class': 'width-form', 'rows': '7'}),
        'color': forms.SelectMultiple(attrs={'class': 'width-form'}),
        'price': forms.NumberInput(attrs={'class': 'width-form'}),
        'size': forms.SelectMultiple(attrs={'class': 'width-form'}),
        'category': forms.Select(attrs={'class': 'width-form'}),
#         'rating': forms.Select(attrs={'class': 'width-form'}),
    }

#     labels = {
#         'category': 'Категория',
#         'mark': 'Марка',
#         'image': 'Изображение',
#         'description': 'Описание',
#         'category_product': 'Категория продукта',
#         'material': 'Материал',
#         'price': 'Цена',
#         'size': 'Размер',
#         'country': 'Страна',
#         'edition': 'Издание',
#         'have': 'Наличие',
#         'characters': 'Характеристики',
#         'date': 'Дата публикации',
#     }
#
#     help_texts = {
#         'price' : 'Введите цену в формате 0.00',
#         'date' : 'Выбери дату публикации'
#     }
