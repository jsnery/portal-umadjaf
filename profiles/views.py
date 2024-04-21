from django.shortcuts import render


def login(request):
    return render(request, 'profiles/pages/login.html')


def register(request):
    return render(request, 'profiles/pages/register.html')


def profile(request):
    return render(
        request,
        'profiles/pages/profile.html',
        context={
            'user': {
                'name': 'John Doe',
                'bio': 'Lorem ipsum dolor sit amet, consectetur adipiscing elit',
                'posts': [
                    {
                        'title': 'Post 1',
                        'content': 'Lorem ipsum dolor sit amet, consectetur adipiscing elit',
                        'date': '01/01/2021',
                        'img': 'https://via.placeholder.com/150'
                    },
                    {
                        'title': 'Post 2',
                        'content': 'Lorem ipsum dolor sit amet, consectetur adipiscing elit',
                        'date': '02/01/2021',
                        'img': 'https://via.placeholder.com/150'
                    },
                    {
                        'title': 'Post 3',
                        'content': 'Lorem ipsum dolor sit amet, consectetur adipiscing elit',
                        'date': '03/01/2021',
                        'img': 'https://via.placeholder.com/150'
                    },
                    {
                        'title': 'Post 4',
                        'content': 'Lorem ipsum dolor sit amet, consectetur adipiscing elit',
                        'date': '04/01/2021',
                        'img': 'https://via.placeholder.com/150'
                    },
                    {
                        'title': 'Post 5',
                        'content': 'Lorem ipsum dolor sit amet, consectetur adipiscing elit',
                        'date': '05/01/2021',
                        'img': 'https://via.placeholder.com/150'
                    },
                    {
                        'title': 'Post 6',
                        'content': 'Lorem ipsum dolor sit amet, consectetur adipiscing elit',
                        'date': '06/01/2021',
                        'img': 'https://via.placeholder.com/150'
                    },
                    {
                        'title': 'Post 7',
                        'content': 'Lorem ipsum dolor sit amet, consectetur adipiscing elit',
                        'date': '07/01/2021',
                        'img': 'https://via.placeholder.com/150'
                    },
                    {
                        'title': 'Post 8',
                        'content': 'Lorem ipsum dolor sit amet, consectetur adipiscing elit',
                        'date': '08/01/2021',
                        'img': 'https://via.placeholder.com/150'
                    },
                    {
                        'title': 'Post 9',
                        'content': 'Lorem ipsum dolor sit amet, consectetur adipiscing elit',
                        'date': '09/01/2021',
                        'img': 'https://via.placeholder.com/150'
                    },
                    {
                        'title': 'Post 10',
                        'content': 'Lorem ipsum dolor sit amet, consectetur adipiscing elit',
                        'date': '10/01/2021',
                        'img': 'https://via.placeholder.com/150'
                    },
                ]
            },
        }
    )
