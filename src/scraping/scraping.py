import requests
from bs4 import BeautifulSoup as Bs
import random

__all__ = ('hh', 'habr', 'superjob')

headers = [
    {
        'User-Agent': 'Mozilla/5.0 (Windows NT 5.1; rv:47.0) Gecko/20100101 Firefox/47.0',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'
    },
    {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:45.0) Gecko/20100101 Firefox/45.0 ',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'
    },
    {
        'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux i686; rv:106.0) Gecko/20100101 Firefox/106.0',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'
    },
]


def hh(url, city=None, language=None):
    jobs = []
    errors = []
    domain = 'https://hh.ru/'
    if url:
        resp = requests.get(url, headers=random.choice(headers))
        if resp.status_code == 200:
            soup = Bs(resp.content, 'html.parser')
            main_div = soup.find('div', attrs={'id': 'a11y-main-content'})
            if main_div:
                div_list = main_div.find_all('div', attrs={'class': 'serp-item'})
                for div in div_list:
                    title = div.find('h3')
                    href = title.a['href']
                    if div.find('div', class_='g-user-content'):
                        description = div.find('div', class_='g-user-content').text
                    else:
                        description = 'Не указано'
                    company = div.find('div', attrs={'class': 'vacancy-serp-item__meta-info-company'}).text
                    if div.find('span', attrs={'class': 'bloko-header-section-3'}):
                        money = div.find('span', attrs={'class': 'bloko-header-section-3'}).text
                    else:
                        money = 'Не указана'
                    jobs.append({'title': title.text,
                                 'url': href,
                                 'description': description,
                                 'company': company,
                                 'money': money,
                                 'city_id': city,
                                 'language_id': language})
            else:
                errors.append({'title': 'DIV does not exists', 'url': url})
        else:
            errors.append({'title': 'Page not response', 'url': url})
    return jobs, errors


def habr(url, city=None, language=None):
    jobs = []
    errors = []
    domain = 'https://career.habr.com'
    if url:
        resp = requests.get(url, headers=random.choice(headers))
        if resp.status_code == 200:
            soup = Bs(resp.content, 'html.parser')
            main_div = soup.find('div', attrs={'class': 'content-wrapper__main--left'})
            if main_div:
                div_list = main_div.find_all('div', attrs={'class': 'vacancy-card__inner'})
                for div in div_list:
                    title = div.find('div', attrs={'class': 'vacancy-card__title'})
                    href = title.a['href']
                    description = div.find('div', attrs={'class': 'vacancy-card__skills'})
                    company = div.find('div', attrs={'class': 'vacancy-card__company-title'}).text
                    jobs.append({'title': title.text,
                                 'url': domain + href,
                                 'description': description.text,
                                 'company': company,
                                 'money': 'Не указана',
                                 'city_id': city,
                                 'language_id': language})
            else:
                errors.append({'title': 'DIV does not exists', 'url': url})
        else:
            errors.append({'title': 'Page not response', 'url': url})
    return jobs, errors


def superjob(url, city=None, language=None):
    jobs = []
    errors = []
    domain = 'https://www.superjob.ru'
    if url:
        resp = requests.get(url, headers=random.choice(headers))
        if resp.status_code == 200:
            soup = Bs(resp.content, 'html.parser')
            main_div = soup.find('div', class_='_3VMkc _3JfmZ UnlTV _3jfFx _3nFmX')
            if main_div:
                div_list = main_div.find_all('div', class_='_3ll9h _26WKs')
                for div in div_list:
                    title = div.find('span', class_='ALb1p _2itH9 _2R-HM _3i61M _2BeAM x_rU7 _1vJ_t DSYVK')
                    href = title.a['href']
                    if div.find('span', class_='_3camv x_rU7 _1vJ_t _2myJ9 _1zaXV'):
                        description = div.find('span', class_='_3camv x_rU7 _1vJ_t _2myJ9 _1zaXV')
                    if div.find('span', class_='_3nMqD f-test-text-vacancy-item-company-name _1v8lV x_rU7 _1vJ_t _2myJ9 _1zaXV'):
                        company = div.find('span', class_='_3nMqD f-test-text-vacancy-item-company-name _1v8lV x_rU7 _1vJ_t _2myJ9 _1zaXV').text
                    else:
                        company = 'Не указана'
                    money = div.find('span', class_='_2eYAG _2BeAM x_rU7 _1vJ_t _2myJ9')

                    jobs.append({'title': title.text,
                                 'url': domain + href,
                                 'description': description.text,
                                 'company': company,
                                 'money': money.text,
                                 'city_id': city,
                                 'language_id': language})
            else:
                errors.append({'title': 'DIV does not exists', 'url': url})
        else:
            errors.append({'title': 'Page not response', 'url': url})
    return jobs, errors


