from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator
from django.contrib import messages
from django.contrib.auth import login, authenticate, logout
from user_profile.forms import LoginForm, RegistrationForm, ChangePasswordForm, ProfileChange
# from .filter import BicycleFilter
# from workspace.decorators import login_required
from django.contrib.auth.hashers import make_password

from market.models import *


from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def rate_product(request, product_id):
    if request.method == 'POST':
        try:
            product = Product.objects.get(id=product_id)
            data = json.loads(request.body)
            rating = int(data.get('rating', 0))

            # Обновляем рейтинг продукта
            product.rating = rating
            product.save()

            return JsonResponse({'success': True})
        except Product.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Product not found'}, status=404)
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)}, status=400)
    return JsonResponse({'success': False, 'error': 'Invalid request'}, status=400)


def main(request):
    products = Product.objects.all()
    categories = Category.objects.all()
    advertising = Advertising.objects.all()
    types = Type.objects.all()

    search = request.GET.get('search', '')
    print(search)

    if search:
        products = products.filter(name__icontains=search)





    title = 'Exclusive.kg'
    return render(request, 'index.html', {
            'products':products,
            'categories': categories,
            'advertising':advertising,
            'types':types,
            'title': title,
            'range': range(1,6),
            'search':search,
            })

def register_profile(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = RegistrationForm()
    return render(request, 'auth/register.html', {'form': form})


def login_profile(request):


    form = LoginForm()
    if request.method == 'POST':
            form = LoginForm(data=request.POST)

            if form.is_valid():
                username = form.cleaned_data.get('username')
                password = form.cleaned_data.get('password')

                user = authenticate(request, username=username, password=password)
                if user:
                    login(request, user)
                    return redirect('/')

    return render(request, 'auth/login.html', {'form': form})


def logout_views(request):
    logout(request)
    return redirect('/')


def profile(request):
    user = request.user
    products = Product.objects.all()

    page_size = int(request.GET.get('limit', 6))
    page = int(request.GET.get('page', 1))
    bicycles = Product.objects.all().order_by('id')

    paginator = Paginator(products, page_size)
    products = paginator.get_page(page)

    return render(request, 'auth/profile.html', {
    'user':user,
    'products':products,

    })

def change_profile(request):

    user = request.user
    if request.method == 'POST':
        form = ProfileChange(request.POST, instance=user)
        if form.is_valid():
            form.save()
            return redirect('profile')
    else:
        form = ProfileChange(instance=user)

    return render(request, 'auth/change_profile.html', {'form':form, 'user':user})


def details(request, id):
    product = get_object_or_404(Product, id=id)
    print(f"Product image path: {product.image.url}")
#     print(f"Product image1 path: {product.image1.url}")
    size = Size.objects.all()
    color = Color.objects.all()
    return render(request, 'details.html', {
        'product': product,
        'size': size,
        'color': color,
        'range':range(1, 6),
    })


def category_elements(request, id):
    category = get_object_or_404(Category, id=id)
    products = Product.objects.filter(category=category)

    return render(request, 'category_elements.html', {
        'category':category,
        'id':id,
        'products':products,
    })

# Create your views here.
