from django.shortcuts import render
from utils.profiles.factory import make_fake_posts, make_fake_users
from profiles.models import UserProfiles, User

# poa = make_fake_users()
post = make_fake_posts()
is_authenticated = False


def login(request):
    return render(
        request,
        'profiles/pages/login.html',
        context={
            'is_authenticated': False
        }
    )


def register(request):
    return render(
        request,
        'profiles/pages/register.html',
        context={
            'is_authenticated': False
        }
    )


def profile(request):
    user = UserProfiles.objects.first()
    print(user)
    profiles = UserProfiles.objects.all()
    for p in profiles:
        for field in p._meta.get_fields():
            print(field.name, ' - ', getattr(p, field.name))

        print('-------------------')
        print(p.user_id.id == user.id)
        print(p.user_id.id, '-', user.id)
        print('-------------------')
        if (p.user_id.id == user.id):
            profile = p

    print(User.objects.filter(id=profile.user_id.id)[0].complete_name)
    return render(
        request,
        'profiles/pages/profile.html',
        context={
            'is_authenticated': is_authenticated,
            'profile': profile,
            'user': User.objects.filter(id=profile.user_id.id)[0],
            'posts': post
        }
    )
