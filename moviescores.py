'''
映画レビューサイトから作品のスコアを取得する。
'''

import requests
from bs4 import BeautifulSoup
import re

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
    res = requests.get(url)
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
        res = get_page(f'{movie_name} 作品情報', sites['EIGA'])

        soup = BeautifulSoup(res.text, 'html.parser')
        # タイトル
        name = soup.find(itemprop='name').string
        # 公開日
        date = soup.find(itemprop='datePublished').get('content')
        # レビュースコア
        rating = soup.find(itemprop='ratingValue').string
        # レビュー数
        count = soup.find(itemprop='reviewCount').string

        ret = {
            'name': name,
            'date': date,
            'rating': float(rating),
            'count': int(count)
        }
    except Exception as e:
        print(e.args)
        print(e.message)
        ret = {}
    return ret


def movies_yahoo(movie_name):
    '''
    Yahoo!映画から作品のスコア、レビュー数を取得する。
    '''
    try:
        pass
        res = get_page(f'{movie_name} 作品', sites['YAHOO'])

        soup = BeautifulSoup(res.text, 'html.parser')
        # レビュースコア
        rating = soup.find(itemprop='ratingValue').string
        count = soup.find(class_='rating-score').find(class_='text-xsmall').string
        # レビュー数
        pattern = r'\d+'
        count = re.search(pattern, count).group(0)

        ret = {
            'rating': float(rating),
            'count': int(count)
        }
    except Exception as e:
        print(e.args)
        print(e.message)
        ret = {}
    return ret


def filmarks_com(movie_name):
    '''
    Filmarksから作品のスコア、レビュー数を取得する。
    '''
    try:
        res = get_page(f'{movie_name} 映画情報', sites['FILMARKS'])

        soup = BeautifulSoup(res.text, 'html.parser')
        # レビュースコアとレビュー数
        desc = soup.find(property='og:description').get('content')
        pattern = r'\d+(?:\.\d+)?'
        ratings = re.findall(pattern, desc)

        ret = {
            'rating': float(ratings[1]),
            'count': int(ratings[0])
        }
    except Exception as e:
        print(e.args)
        print(e.message)
        ret = {}
    return ret
