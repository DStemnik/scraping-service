from django.shortcuts import render
from .models import Vacancy
from .form import FindForm


def home_view(request):
    # print(request.GET['city'], request.GET['language'])
    form = FindForm()
    city = request.GET.get('city')
    language = request.GET.get('language')
    data = {}
    qs = {}
    if city:
        data = {'city__slug': city}
    if language:
        data = {'language__slug': language}
    if len(data) > 0:
        qs = Vacancy.objects.filter(**data)
    return render(request, 'scraping/home.html', context={'object_list': qs, 'form': form})

