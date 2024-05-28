from faker import Faker
from random import randint


fake = Faker('pt_BR')


def rand_ratio():
    return randint(360, 540), randint(540, 720)


def make_fake_posts():
    posts = []
    for i in range(1, 19):
        posts.append({
            'title': fake.text(max_nb_chars=90),
            'content': fake.text(max_nb_chars=500),
            'date': fake.date(pattern='%d/%m/%Y'),
            'img': 'https://loremflickr.com/%s/%s/culto+evangelico' % rand_ratio()
        })

    return posts


def make_fake_users():
    users = {
        'id': int(fake.random_number(digits=9999)),
        'name': fake.name(),
        'avatar': {'url': 'https://loremflickr.com/500/500/rosto'},
        'bio': fake.sentence(nb_words=30),
        'posts': make_fake_posts()
    }

    return users


def make_fake_pedidos():
    pedidos = []
    for i in range(1, 10):  # Gera 10 pedidos falsos
        pedido = {
            'id': int(fake.random_number(digits=9999)),
            'titulo': fake.sentence(nb_words=5),
            'img': {
                'url': f'cart/src/products/{i}.webp'
            },
            'data': fake.date(pattern='%d/%m/%Y'),
        }
        pedidos.append(pedido)

    return pedidos
