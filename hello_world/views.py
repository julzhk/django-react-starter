from django.shortcuts import render


def home(request):
    return render(request, 'hello_world/home.html', {})
