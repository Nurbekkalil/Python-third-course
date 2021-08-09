import datetime

from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from product.models import Product, ConfirmCode
from product.forms import ProductForm, RegisterForm
from django.contrib import auth
from .forms import LoginForm
# Create your views here.

def hello_world_view(request):
    return HttpResponse ('<h1>Hello World!!!</h1>')


def main_page_view(request):
    product = Product.objects.all()
    data = {
        'title': 'Main Page',
        'list': [1, 2, 3, 4],
        'product_list': product
    }
    return render(request, 'index.html', context=data)


def product_item_view(request, product_id):
    product = Product.objects.get(id=product_id)
    product_list = Product.objects.all()


    data = {
        'product': product,
        'title': product.title,
        'product_list': product_list

    }
    return render(request, 'item.html', context=data)


@login_required(login_url='/login/')

def add_product(request):
    if request.method == 'GET':
        data = {
            'form': ProductForm()
        }
        return render(request, 'add.html', context=data)
    elif request.method == 'POST':
        form = ProductForm(data=request.POST)
        if form.is_valid():
            form.save()
            return redirect('/')


def logout(request):
    auth.logout(request)
    return redirect('/login/')


def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = auth.authenticate(username=username, password=password)
        if user is not None:
            auth.login(request, user)
    data = {
        'form': LoginForm()
    }
    return render(request, 'login.html', context=data)


def register(request):
    if request.method == 'POST':
        form = RegisterForm(data=request.POST)
        if form.is_valid():
            form.save()
            return redirect('/login/')
        else:
            data = {
                'form': form
            }
            return render(request, 'register.html', context=data)
    data = {
        'form': RegisterForm()

    }
    return render(request, 'register.html', context=data)


def search(request):
    query = request.GET.get('query', '')
    print(query)
    return JsonResponse(data={'key': query}, safe=False)


def activate(request, code):
    print(code)
    try:
        user = ConfirmCode.objects.get(code=code,
                                       valid_until__gte=datetime.datetime.now()).user

        user.is_active = True
        user.save()
    except:
        pass
    return redirect('/login/')
