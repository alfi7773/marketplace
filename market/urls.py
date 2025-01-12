from market import views
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('login/', views.login_profile, name='login'),
    path('register/', views.register_profile, name='register'),
    path('logout/', views.logout_views, name='logout'),
    path('profile/', views.profile, name='profile'),
    path('change-profile/', views.change_profile, name='change'),
    path('products/<int:id>/', views.details, name='details'),
    path('rate-product/<int:product_id>/', views.rate_product, name='rate_product'),
    path('category/<int:id>/', views.category_elements, name='category'),
]


urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
