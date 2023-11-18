from django.shortcuts import render

# Create your views here.


def index(request):
    data = {
        'title': 'FLAGMAN',
    }

    return render(request, 'home/index.html', context=data)
