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
    I'm Feeling Luckeyを利用。
    '''
    BASE_URL = 'https://www.google.co.jp/search'
    q = text.replace(' ', '+')
    query = f'?q={q}+site%3A{site}&ie=UTF-8&btnI=I%27m+Feeling+Lucky'
    url = BASE_URL + query
    res = requests.get(url)
    res.encoding = res.apparent_encoding
    return res


def eiga_com(movie_name):
    '''
    映画.comから作品のタイトル、公開日、スコア、レビュー数を取得する。
    '''
    res = get_page(f'{movie_name}+作品情報', sites['EIGA'])

    soup = BeautifulSoup(res.text, 'html.parser')
    # タイトル
    name = soup.find(itemprop='name').string
    # 公開日
    date = soup.find(itemprop='datePiublished').get('content')
    # レビュースコア
    rating = soup.find(itemprop='ratingValue').string
    # レビュー数
    count = soup.find(itemprop='reviewCount').string

    ret = {
        'name': name,
        'date': date,
        'rating': rating,
        'count': count
    }
    return ret


def movies_yahoo(movie_name):
    '''
    Yahoo!映画から作品のスコア、レビュー数を取得する。
    '''
    res = get_page(f'{movie_name}+作品', sites['YAHOO'])

    soup = BeautifulSoup(res.text, 'html.parser')
    # レビュースコア
    rating = soup.find(itemprop='ratingValue').string
    count = soup.find(class_='rating-score').find(class_='text-xsmall').string
    # レビュー数
    pattern = r'\d+'
    count = re.search(pattern, count).group(0)

    ret = {
        'rating': rating,
        'count': count
    }
    return ret


def filmarks_com(movie_name):
    '''
    Filmarksから作品のスコア、レビュー数を取得する。
    '''
    res = get_page(movie_name, sites['FILMARKS'])

    soup = BeautifulSoup(res.text, 'html.parser')
    # レビュースコアとレビュー数
    desc = soup.find(property='og:description').get('content')
    pattern = r'\d+(?:\.\d+)?'
    ratings = re.findall(pattern, c)

    ret = {
        'rating': ratings[1],
        'count': ratings[0]
    }
    return ret
