import re
import movielist
import moviescores
import twittersearch
import negaposi


def format_text(text):
    fmt_text = text.replace('\r', ' ').replace('\n', ' ').replace(
        '\t', ' ').replace('\f', ' ').replace('\v', ' ')
    fmt_text = re.sub(
        r'https?(:\/\/[-_\.!~*\'()a-zA-Z0-9;\/?:\@&=\+\$,%#]+)', '', fmt_text)


def main():
    movies = movielist.movie_list()
    for movie in movies:
        name = movie['name'].replace(' ', '+')
        movie['eiga'] = moviescores.eiga_com(name)
        movie['yahoo'] = moviescores.movies_yahoo(name)
        movie['filmarks'] = moviescores.filmarks_com(name)

        opt = '-source:filmarks -source:twittbot.net -filter:verified'
        q = f'{movie['name']} {opt}'
        tweets = twittersearch.search(
            q, since=movie['eiga']['date'], count=200)

        movie['tweets'] = []
        pn_dict = negaposi.set_dict()
        for tweet in tweets:
            if not tweet['entities']['urls']:
                tweet_text = format_text(tweet['full_text'])
                negaposi.get_nega_posi(tweet_text, pn_dict)
                movie['tweets'].append({'text': tweet_text, 'score': score})


if __name__ == '__main__':
    main()
