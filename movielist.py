import tohocinemas
import unicodedata


def movie_list():
    showing = tohocinemas.showing_list()
    movies = []
    for movie in showing['data']:
        name = unicodedata.normalize('NFKC', movie['name'])
        desc = tohocinemas.movie_desc(movie['mcode'])
        if '<br>' in desc:
            desc = desc.split('<br>')[1]
        movies.append({'name': name, 'desc': desc})

    return movies


def main():
    print(movie_list())


if __name__ == '__main__':
    main()
