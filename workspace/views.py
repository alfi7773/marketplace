from django.shortcuts import render, redirect, get_object_or_404
from workspace.forms import ProductForm

from market.models import *

def workspace(request):
        user = request.user
        products = Product.objects.all()
        return render(request, 'workspace/index.html', {
        'user':user,
        'products':products,

        })


def create(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('workspace')
    else:
            form = ProductForm()

    return render(request, 'workspace/create.html', {'form': form})



def update(request, id):
    product = get_object_or_404(Product, id=id)
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            return redirect('workspace')
    else:
        form = ProductForm(instance=product)

    return render(request, 'workspace/update.html', {'form': form, 'id': id})


def delete(request, id):
    products = get_object_or_404(Product, id=id)
    products.delete()
    return redirect('workspace')



# Create your views here.

