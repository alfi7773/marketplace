from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator
from django.contrib import messages
from django.contrib.auth import login, authenticate, logout
from user_profile.forms import LoginForm, RegistrationForm, ChangePasswordForm, ProfileChange, ProductRatingForm
from .filter import ProductFilter
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


    title = 'Exclusive.kg'
    return render(request, 'index.html', {
            'products':products,
            'categories': categories,
            'advertising':advertising,
            'types':types,
            'title': title,
            'range': range(1,6)
            })

def catalogue(request):
    products = Product.objects.all()
    categories = Category.objects.all()
    advertising = Advertising.objects.all()
    types = Type.objects.all()

    search = request.GET.get('search')
    if search:
        products = products.filter(name__icontains=search)

    filter_set = ProductFilter(data=request.GET, queryset=products)
    products = filter_set.qs

    try:
        page_size = int(request.GET.get('limit', 6))
    except ValueError:
        page_size = 6
    page = int(request.GET.get('page', 1))

    paginator = Paginator(products, page_size)
    products = paginator.get_page(page)

    return render(request, 'catalogue.html', {
        'products': products,
        'categories': categories,
        'advertising': advertising,
        'types': types,
        'range': range(1, 6),
        'filter': filter_set,
    })


def register_profile(request):
    if request.user.is_authenticated:
            return redirect('/')

    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
                user = form.save()
                login(request, user)
                return redirect('workspace')
    else:
        form = RegistrationForm()

    return render(request, 'auth/register.html', {'form': form})

    # Create your views here.


def login_profile(request):
    if request.user.is_authenticated:
            return redirect('/')

    form = LoginForm()
    if request.method == 'POST':
            form = LoginForm(data=request.POST)

            if form.is_valid():
                username = form.cleaned_data.get('username')
                password = form.cleaned_data.get('password')

                # user = User.objects.filter(username=username).first()
                # if user and user.check_password(password):
                user = authenticate(username=username, password=password)
                if user:
                    login(request, user)

                    return redirect('workspace')

                messages.error(request, 'The user is not found or the password is incorrect.')

    return render(request, 'auth/login.html', {'form': form})


def logout_views(request):
    logout(request)
    return redirect('/')


def profile(request):
    user = request.user
    products = Product.objects.filter(author=request.user).order_by('name')

    page_size = int(request.GET.get('limit', 6))
    page = int(request.GET.get('page', 1))
#     products = Product.objects.all().order_by('id')

    paginator = Paginator(products, page_size)
    products = paginator.get_page(page)

    return render(request, 'auth/profile.html', {
    'user':user,
    'products':products,
    'range':range(1,6)
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

def change_password(request):
    form = ChangePasswordForm()

    if request.method == 'POST':
        form = ChangePasswordForm(data=request.POST, user=request.user)
        if form.is_valid():
            new_password = form.cleaned_data.get('new_password')
            user = request.user
            # user.password = make_password(new_password)
            user.set_password(new_password)
            user.save()

            login(request, user)

#             messages.success(request, 'The password was modified successfully.')
            return redirect('workspace')

    return render(request, 'auth/change_password.html', {'form': form})


def details(request, id):
    product = get_object_or_404(Product, id=id)
    products = Product.objects.all()

#     user_rating = ProductRating.objects.filter(product=product, user=request.user).first()

    if request.method == 'POST' and request.user.is_authenticated:
        form = ProductRatingForm(request.POST)
        if form.is_valid():
            if user_rating:
                user_rating.rating = form.cleaned_data['rating']
                user_rating.save()
            else:
                ProductRating.objects.create(
                    product=product,
                    user=request.user,
                    rating=form.cleaned_data['rating']
                )
            product.total_rating = sum([r.rating for r in product.ratings.all()])
            product.total_reviews = product.ratings.count()
            product.save()

            return redirect('details', id=id)
    else:
        form = ProductRatingForm()

    # Получаем средний рейтинг товара
    average_rating = product.get_average_rating()

    return render(request, 'details.html', {
        'product': product,
        'products': products,
        'form': form,
        'average_rating': average_rating,
        'range': range(1, 6),
    })


def category_elements(request, id):
    category = get_object_or_404(Category, id=id)
    products = Product.objects.filter(category=category)

    return render(request, 'category_elements.html', {
        'category':category,
        'id':id,
        'products':products,
        'range': range(1, 6)
    })

def type_elements(request, id):
    type = get_object_or_404(Type, id=id)
    products = Product.objects.filter(types=type)

    return render(request, 'types_elements.html', {
        'type':type,
        'id':id,
        'products':products,
        'range': range(1,6)
    })

def reklama(request):
    products = Product.objects.filter(category__name='Electronics')

    return render(request, 'reklama.html', {
    'products':products,
    })
# Create your views here.
