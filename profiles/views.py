from django.shortcuts import render
from utils.profiles.factory import make_fake_users


user = make_fake_users()
is_authenticated = True


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
    return render(
        request,
        'profiles/pages/profile.html',
        context={
            'is_authenticated': is_authenticated,
            'user': user
        }
    )
