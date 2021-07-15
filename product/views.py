from django.http import HttpResponse
from django.shortcuts import render
from product.models import Product
# Create your views here.

def hello_world_view(request):
    return HttpResponse ('<h1>Hello World!!!</h1>')


def main_page_view(request):
    product = Product.objects.all()
    print(product)
    for i in product:
        print('ID:', i.id)
        print('Title',i.title)
        print('Price:', i.price)
        print()
    data = {
        'title': 'Main Page',
        'list': [1, 2, 3, 4],
        'product_list': product
    }
    return render(request, 'index.html', context=data)


def product_item_view(request, product_id):
    product = Product.objects.get(id=product_id)
    data = {
        'product': product,
        'title': product.title
    }
    return render(request, 'item.html', context=data)