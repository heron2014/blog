from django.shortcuts import render


def home(request):
    if request.user.is_authenticated():

        context = {'title': 'Welcome to my new website',
                    'myUser': request.user}
    else:
        context = {'title': 'Hello stranger'}

    return render(request, 'blog/home.html', context)