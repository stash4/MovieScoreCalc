'''
TwitterのStanderd search APIを使用する。
'''

from requests_oauthlib import OAuth1Session
import urllib
import settings

keys = settings.keys

twitter = OAuth1Session(
    keys['CONSUMER_KEY'],
    keys['CONSUMER_SECRET'],
    keys['ACCESS_TOKEN'],
    keys['ACCESS_TOKEN_SECRET']
)


def search(words, since='', count=100):
    '''
    キーワード、期間、ツイート数を指定してTwitter検索を行う。
    '''
    url = 'https://api.twitter.com/1.1/search/tweets.json'
    if since:
        since = f'since: {since}'
    q = f'{words} -RT {since}'
    if count > 100:
        res_count = 100
        req_count = count / 100
    else:
        res_count = count
        req_count = 1

    params = {
        'q': q,
        'result_type': 'recent',
        'tweet_mode': 'extended',
        'count': res_count
    }

    results = []

    for _ in range(req_count):
        res = twitter.get(url, params=params)
        res_json = res.json()

        for status in res_json['statuses']:
            results.append(status)

        if not ('next_results' in res_json['search_metadata']):
            break
        else:
            params = urllib.parse.parse_qs(
                res_json['search_metadata']['next_results'][1:])
            params['tweet_mode'] = 'extended'

    return results
