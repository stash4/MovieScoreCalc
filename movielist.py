'''
TOHOシネマズの上映中作品リストを取得する。
'''
import tohocinemas
import unicodedata


def movie_list():
    '''
    TOHOシネマズで上映中の作品の、タイトルと説明を取得する。
    '''
    showing = tohocinemas.showing_list()
    movies = []
    for movie in showing['data']:
        name = unicodedata.normalize('NFKC', movie['name'])
        desc, name_en = tohocinemas.movie_desc(movie['mcode'])
        im_url = tohocinemas.movie_image_url(movie)
        if '<br>' in desc:
            if '正式タイトル：' in desc:
                name, desc = desc.split('正式タイトル：')[1].split('<br>')
            else:
                desc = desc.split('<br>')[1]
        movies.append({
            'name': name,
            'desc': desc,
            'name_en': name_en,
            'image': im_url})

    return movies


def main():
    print(movie_list())


if __name__ == '__main__':
    main()
