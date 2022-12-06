# -*- coding: utf-8 -*-
import os
import django

#  you have to set the correct path to you settings module
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "scraping_service.settings")
django.setup()

from scraping.scraping import *
from scraping.models import Vacancy, City, Language, Error, Url
from django.db import DatabaseError
from django.contrib.auth import get_user_model
import asyncio


User = get_user_model()

parsers = (
    (hh, 'hh'),
    (habr, 'habr'),
    (superjob, 'superjob'),
           )


def get_settings():
    qs = User.objects.filter(send_email=True).values()
    settings_lst = set((q['city_id'], q['language_id']) for q in qs)
    return settings_lst


def get_urls(_settings):
    qs = Url.objects.all().values()
    url_dct = {(q['city_id'], q['language_id']): q['url_data'] for q in qs}
    urls = []
    for pair in url_dct:
        tmp = {}
        tmp['city'] = pair[0]
        tmp['language'] = pair[1]
        tmp['url_data'] = url_dct[pair]
        urls.append(tmp)
    return urls


settings = get_settings()
url_list = get_urls(settings)

jobs, errors = [], []

# 6sec
# for data in url_list:
#     for func, key in parsers:
#         url = data['url_data'][key]
#         j, e = func(url, city=data['city'], language=data['language'])
#         jobs += j
#         errors += e


async def pars(value):
    # Выполняем функцию ассинронно (func, *args, **kwargs)
    # Вместо loop.run_in_execute()
    job, err = await asyncio.to_thread(*value)
    errors.extend(err)
    jobs.extend(job)

async def main():
    task = [
        (func, data['url_data'][key], data['city'], data['language'])
        for data in url_list
        for func, key in parsers
    ]
    tasks = [pars(f) for f in task]
    await asyncio.gather(*tasks)

asyncio.run(main())

for job in jobs:
    v = Vacancy(**job)
    try:
        v.save()
    except DatabaseError:
        pass
