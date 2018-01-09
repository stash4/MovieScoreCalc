import re
import numpy
import pickle
import movielist
import moviescores
import twittersearch
import negaposi


def format_text(text):
    '''
    文字列から改行文字とURLを除去
    '''
    fmt_text = text.replace('\r', ' ').replace('\n', ' ').replace(
        '\t', ' ').replace('\f', ' ').replace('\v', ' ')
    fmt_text = re.sub(
        r'https?(:\/\/[-_\.!~*\'()a-zA-Z0-9;\/?:\@&=\+\$,%#]+)', '', fmt_text)
    return fmt_text


def normalize_num(num_list, maximum=1):
    '''
    最大値を指定して数値を正規化
    '''
    s = numpy.array(num_list)
    smin = s.min()
    smax = s.max()
    n_s = (s - smax).astype(float) / (smax - smin).astype(float)
    ret = list(n_s * maximum)
    return ret


def main():
    # 作品リスト取得
    movies = movielist.movie_list()
    for movie in movies:
        # 各作品のレビュースコア取得
        name = movie['name'].replace(' ', '+')
        movie['eiga'] = moviescores.eiga_com(name)
        movie['yahoo'] = moviescores.movies_yahoo(name)
        movie['filmarks'] = moviescores.filmarks_com(name)

        # 各作品に関するツイート取得
        opt = '-source:filmarks -source:twittbot.net -filter:verified'
        q = f'{movie["name"]} {opt}'
        tweets = twittersearch.search(
            q, since=movie['eiga']['date'], count=200)

        # 各ツイートのネガポジ判定
        movie['tweets'] = []
        pn_dict = negaposi.set_dict()
        for tweet in tweets:
            if not tweet['entities']['urls']:
                sc_name = tweet['user']['screen_name']
                tw_id = tweet['id_str']
                tw_url = f'https://https://twitter.com/{sc_name}/{tw_id}'
                tw_text = format_text(tweet['full_text'])
                score = negaposi.get_nega_posi(tw_text, pn_dict)
                tw = {'url': tw_url, 'text': tw_text, 'score': score}
                movie['tweets'].append(tw)

    # ツイートのスコア計算
        scores = []
        for tweet in movie['tweets']:
            scores.append(tweet['score'])
        n_scores = normalize_num(scores, maximum=5)
        s = sum(n_scores)
        N = len(n_scores)
        mean = s / N
        movie['twitter'] = {'rating': mean, 'count': N}

        # 総合スコア計算
        eiga_c = movie['eiga']['count']
        eiga_w = movie['eiga']['rating'] * eiga_c
        yahoo_c = movie['yahoo']['count']
        yahoo_w = movie['yahoo']['rating'] * yahoo_c
        filmarks_c = movie['filmarks']['count']
        filmarks_w = movie['filmarks']['rating'] * filmarks_c
        twitter_c = movie['twitter']['count']
        twitter_w = movie['twitter']['rating'] * twitter_c
        count = eiga_c + yahoo_c + filmarks_c + twitter_c
        rating = (eiga_w + yahoo_w + filmarks_w + twitter_w) / counts
        movie['total'] = {'rating': rating, 'count': count}


if __name__ == '__main__':
    main()
