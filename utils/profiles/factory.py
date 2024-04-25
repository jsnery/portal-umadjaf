from faker import Faker
from random import randint


fake = Faker('pt_BR')


def rand_ratio():
    return randint(360, 540), randint(540, 720)


def make_fake_posts():
    posts = []
    for i in range(1, 19):
        posts.append({
            'title': f'Post {i}',
            'content': fake.text(max_nb_chars=500),
            'date': fake.date(pattern='%d/%m/%Y'),
            'img': 'https://loremflickr.com/%s/%s/pregador' % rand_ratio()
        })

    return posts


def make_fake_users():
    users = {
        'name': fake.name(),
        'avatar': {'url': 'https://loremflickr.com/500/500/rosto'},
        'bio': fake.sentence(nb_words=30),
        'posts': make_fake_posts()
    }

    return users
