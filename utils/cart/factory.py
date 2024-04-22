from faker import Faker
from random import uniform, randint


fake = Faker('pt_BR')


def rand_ratio():
    return randint(1000, 9999)


def make_fake_products():
    products = {}
    for i in range(1, 10):
        products[f'{str(i)}'] = {
            'name': f'Bíblia Sagrada {' '.join(fake.words(nb=2))}',
            'last_price': round(uniform(80, 100), 2),
            'price': round(uniform(40, 80), 2),
            'brief_description': fake.sentence(nb_words=30),
            'description': fake.text(max_nb_chars=500),
            'image': {
                'url': f'cart/src/products/{i}.webp'
            },
        }

    return products
