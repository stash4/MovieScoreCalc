'''
映画レビューサイトから作品のスコアを取得する。
'''

import requests
from bs4 import BeautifulSoup
import re
import urllib.parse

sites = {
    'EIGA': 'eiga.com',
    'YAHOO': 'movies.yahoo.co.jp',
    'FILMARKS': 'filmarks.com'
}


def get_page(text, site):
    '''
    キーワードとサイトを指定してGoogle検索でトップのページを取得する。
    # I'm Feeling Luckeyを利用。
    '''
    BASE_URL = 'https://www.google.co.jp/search'
    q = text.replace(' ', '+').replace('&', '%26')
    # query = f'?q={q}+site%3A{site}&ie=UTF-8&btnI=I%27m+Feeling+Lucky'
    query = f'?q={q}+site:{site}&ie=UTF-8'
    url = BASE_URL + query
    print(url)
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_2)'}
    res = requests.get(url, headers=headers)
    res.encoding = res.apparent_encoding

    google_soup = BeautifulSoup(res.text, 'html.parser')
    href = google_soup.find(class_='r').select('a')[0].get('href')
    pattern = r'http(s)?://' + site + r'/movie(s)?(/[a-zA-Z0-9%]*)?/[0-9]*'
    href = re.search(pattern, href).group(0)
    print(href)
    ret = requests.get(href)
    return ret


def eiga_com(movie_name):
    '''
    映画.comから作品のタイトル、公開日、スコア、レビュー数を取得する。
    '''
    try:
        # サイト内検索
        movie_name = movie_name.replace('/', ' ')
        q = urllib.parse.quote(movie_name)
        result = requests.get(f'http://eiga.com/search/{q}/')
        result_sp = BeautifulSoup(result.text, 'html.parser')
        href = result_sp.find(id='rslt-movie').select('a')[0].get('href')
        url = f'http://eiga.com{href}'

        detail = requests.get(url)
        detail_sp = BeautifulSoup(detail.text, 'html.parser')
        # タイトル
        name = detail_sp.find(itemprop='name').string
        # 公開日
        date = detail_sp.find(itemprop='datePublished').get('content')
        # レビュースコア
        rating = detail_sp.find(itemprop='ratingValue').string
        # レビュー数
        count = detail_sp.find(itemprop='reviewCount').string

        ret = {
            'name': name,
            'date': date,
            'rating': float(rating),
            'count': int(count)
        }
    except Exception as e:
        ret = {}
    return ret


def movies_yahoo(movie_name):
    '''
    Yahoo!映画から作品のスコア、レビュー数を取得する。
    '''
    try:
        q = urllib.parse.quote(movie_name)
        result = requests.get(f'https://movies.yahoo.co.jp/search/?query={q}')
        result_sp = BeautifulSoup(result.text, 'html.parser')
        href = result_sp.find(id='rsltmv').select('a')[0].get('href')
        url = f'https://movies.yahoo.co.jp{href}'

        detail = requests.get(url)
        detail_sp = BeautifulSoup(detail.text, 'html.parser')

        # レビュースコア
        rating = detail_sp.find(itemprop='ratingValue').string
        count = detail_sp.find(class_='rating-score').find(class_='text-xsmall').string
        count = count.replace(',', '')
        # レビュー数
        pattern = r'\d+'
        count = re.search(pattern, count).group(0)

        ret = {
            'rating': float(rating),
            'count': int(count)
        }
    except Exception as e:
        ret = {}
    return ret


def filmarks_com(movie_name):
    '''
    Filmarksから作品のスコア、レビュー数を取得する。
    '''
    try:
        q = urllib.parse.quote(movie_name)
        result = requests.get(f'https://filmarks.com/search/movies?q={q}')
        result_sp = BeautifulSoup(result.text, 'html.parser')
        href = result_sp.find(class_='p-movies-grid').select('a')[0].get('href')
        url = f'https://filmarks.com{href}'

        detail = requests.get(url)
        detail_sp = BeautifulSoup(detail.text, 'html.parser')
        # レビュースコアとレビュー数
        desc = detail_sp.find(property='og:description').get('content')
        pattern = r'\d+(?:\.\d+)?'
        ratings = re.findall(pattern, desc)

        ret = {
            'rating': float(ratings[1]),
            'count': int(ratings[0])
        }
    except Exception as e:
        ret = {}
    return ret
