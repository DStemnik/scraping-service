from django.shortcuts import render
from .models import Vacancy
from .form import FindForm
from django.core.paginator import Paginator


# def home_view(request):
#     # print(request.GET['city'], request.GET['language'])
#     form = FindForm()
#     city = request.GET.get('city')
#     language = request.GET.get('language')
#     data = {}
#     qs = {}
#     if city:
#         data = {'city__slug': city}
#     if language:
#         data = {'language__slug': language}
#     if len(data) > 0:
#         qs = Vacancy.objects.filter(**data)
#     return render(request, 'scraping/home.html', context={'object_list': qs, 'form': form})

def home_view(request):
    if request.user.is_authenticated:
        user = request.user
        form = FindForm(initial={
            'city': user.city,
            'language': user.language}
        )
    else:
        form = FindForm()
    return render(request, 'scraping/home.html', context={'form': form})

def list_view(request):
    # print(request.GET['city'], request.GET['language'])
    form = FindForm()
    city = request.GET.get('city')
    language = request.GET.get('language')
    data = {}
    page_obj = {}
    context = {'city': city, 'language': language, 'form': form}
    if city:
        data = {'city__slug': city}
    if language:
        data = {'language__slug': language}
    if len(data) > 0:
        qs = Vacancy.objects.filter(**data)
        paginator = Paginator(qs, 10)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        context['object_list'] = page_obj
    return render(request, 'scraping/list.html', context)

