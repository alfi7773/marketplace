from django.contrib import admin
from .models import *
from django.utils.safestring import mark_safe


admin.site.register(Category)
admin.site.register(Color)
admin.site.register(Size)
admin.site.register(Advertising)
admin.site.register(Type)

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'rating', 'price', 'get_image')
    readonly_fields = ('view', 'get_full_image')

    @admin.display(description='изображение')
    def get_image(self, product):
        return mark_safe(f'<img src="{product.image.url}" width="100px">')

    @admin.display(description='изображение')
    def get_full_image(self, product):
        return mark_safe(f'<img src="{product.image.url}" width="75%">')


# Register your models here.
