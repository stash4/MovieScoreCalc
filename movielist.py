'''
TOHOシネマズの上映中作品リストを取得する。
'''
import tohocinemas
import unicodedata
import re


def movie_list():
    '''
    TOHOシネマズで上映中の作品の、タイトルと説明を取得する。
    '''
    showing = tohocinemas.showing_list()
    movies = []
    for movie in showing['data']:
        name = unicodedata.normalize('NFKC', movie['name'])
        mcode = movie['mcode']
        desc, name_en = tohocinemas.movie_desc(mcode)
        im_url = tohocinemas.movie_image_url(movie)
        if '正式タイトル：' in desc:
            pattern = r'(正式タイトル[：?|:])(.*)(<br/?>)'
            s = re.search(pattern, desc)
            name = s.group(2)
            desc = desc.replace(s.group(0), '')
            tag_p = r'<.*?>'
            desc = re.sub(tag_p, '', desc)

        movies.append({
            'name': name,
            'desc': desc,
            'name_en': name_en,
            'image': im_url,
            'mcode': mcode})

    return movies


def main():
    print(movie_list())


if __name__ == '__main__':
    main()
