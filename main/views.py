from django.shortcuts import render

from goods.models import Categories

def index(request):
    return render(request, 'main/index.html')

def about(request):
    return render(request, 'main/about.html')

def services(request):
    return render(request, 'main/services.html')

def SMM(request):
    return render(request, 'main/SMM.html')

