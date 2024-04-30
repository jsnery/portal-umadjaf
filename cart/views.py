from django.shortcuts import render
from utils.cart.factory import make_fake_products


produtos = make_fake_products()
is_authenticated = False


def store(request):
    return render(
        request,
        'cart/pages/store.html',
        context={
            'is_authenticated': is_authenticated,
            'products_partial': produtos,
            'page': 'store',
            'carousel': {
                'card1': {
                    'image': {'url': 'cart/src/banners/1.png'},
                    'title': 'Bíblia Sagrada Flores Creme',
                    'id_link': '1'
                },
                'card2': {
                    'image': {'url': 'cart/src/banners/2.png'},
                    'title': 'Fardamento Umafjaf',
                    'id_link': '2'
                },
                'card3': {
                    'image': {'url': 'cart/src/banners/3.png'},
                    'title': 'Banda',
                    'id_link': '3'
                }
            },
        }
    )


def product(request, id):
    return render(
        request,
        'cart/pages/product.html',
        context={
            'is_authenticated': is_authenticated,
            'product': produtos[id],
            'products_partial': produtos,
        }
    )
