from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.
def index(request):  #ссылка на HttpRequest - инфа о запросе: сессии, куки
    return HttpResponse("Страница приложения women.")

def categories(request):
    return HttpResponse("<h1>Статьи по категориям<h1>")