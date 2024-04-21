from django.shortcuts import render


def store(request):
    return render(
        request,
        'cart/pages/store.html',
        context={
            'products': [
                {
                    'image': {'url': 'src/store/products/1.webp'},
                    'name': 'Biblia 1',
                    'last_price': '100,00',
                    'price': '50,00',
                    'description': 'This is the content of news 1.'
                },
                {
                    'image': {'url': 'src/store/products/2.webp'},
                    'name': 'Biblia 2',
                    'last_price': '100,00',
                    'price': '50,00',
                    'description': 'This is the content of news 2.'
                },
                {
                    'image': {'url': 'src/store/products/3.webp'},
                    'name': 'Biblia 3',
                    'last_price': '100,00',
                    'price': '50,00',
                    'description': 'This is the content of news 3.'
                },
                {
                    'image': {'url': 'src/store/products/1.webp'},
                    'name': 'Biblia 4',
                    'last_price': '100,00',
                    'price': '50,00',
                    'description': 'This is the content of news 4.'
                },
                {
                    'image': {'url': 'src/store/products/2.webp'},
                    'name': 'Biblia 5',
                    'last_price': '59,90',
                    'price': '49,90',
                    'description': 'This is the content of news 5.'
                },
                {
                    'image': {'url': 'src/store/products/3.webp'},
                    'name': 'Biblia 6',
                    'last_price': '100,00',
                    'price': '50,00',
                    'description': 'This is the content of news 6.'
                },
                {
                    'image': {'url': 'src/store/products/1.webp'},
                    'name': 'Biblia 7',
                    'last_price': '100,00',
                    'price': '50,00',
                    'description': 'This is the content of news 7.'
                },
                {
                    'image': {'url': 'src/store/products/2.webp'},
                    'name': 'Biblia 8',
                    'last_price': '100,00',
                    'price': '50,00',
                    'description': 'This is the content of news 8.'
                },
                {
                    'image': {'url': 'src/store/products/3.webp'},
                    'name': 'Biblia 9',
                    'last_price': '100,00',
                    'price': '50,00',
                    'description': 'This is the content of news 9.'
                }
            ],
            'carousel': {
                'card1': {
                    'image': {'url': 'src/store/banners/1.png'},
                    'title': 'Membro',
                },
                'card2': {
                    'image': {'url': 'src/store/banners/2.png'},
                    'title': 'Coordenação',
                },
                'card3': {
                    'image': {'url': 'src/store/banners/3.png'},
                    'title': 'Banda',
                }
            },
        }
    )
