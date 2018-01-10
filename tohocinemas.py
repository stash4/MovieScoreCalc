'''
TOHOシネマズの非公開APIとWebページから作品情報を取得する。
'''

import requests
from datetime import datetime
from bs4 import BeautifulSoup

BASE_URL = 'https://hlo.tohotheater.jp/'


def showing_list():
    '''
    上映中の作品のjsonを返す。
    https://hlo.tohotheater.jp/data_net/json/movie/TNPI3090.JSON?_dc=:unix_time
    '''
    unix_time = datetime.now().strftime('%s')
    url = f'{BASE_URL}data_net/json/movie/TNPI3090.JSON?_dc={unix_time}'

    res = requests.get(url)
    res.encoding = res.apparent_encoding
    return res.json()


def movie_desc(mcode):
    '''
    mcodeを指定して映画の詳細ページを取得。そこから映画の説明と英語のタイトルを抜き出して返す。
    https://hlo.tohotheater.jp/net/movie/TNPI3060J01.do?sakuhin_cd=:mcode
    '''
    url = f'{BASE_URL}net/movie/TNPI3060J01.do?sakuhin_cd={mcode}'
    detail = requests.get(url)
    detail.encoding = detail.apparent_encoding

    detail_soup = BeautifulSoup(detail.text, 'html.parser')
    desc = detail_soup.find(property='og:description').get('content')
    name_en = detail_soup.find(class_='en theater-detail-word-break').string
    return desc, name_en
