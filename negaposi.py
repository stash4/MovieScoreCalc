'''
極性辞書を用いて、文字列のネガポジ判定を行う。
形態素解析にはMeCabを使用する。
極性辞書は、以下のページで公開されている日本語評価極性辞書を使用する。
    Open Resources/Japanese Sentiment Polarity Dictionary
    - 東北大学 乾・岡﨑研究室 / Communication Science Lab, Tohoku University
    http://www.cl.ecei.tohoku.ac.jp/index.php?Open%20Resources/Japanese%20Sentiment%20Polarity%20Dictionary
'''
import MeCab

score = {
    'POSI': 1,
    'NEGA': -1,
    'EQUAL': 0
}

pn_path = {
    'VERBS': '../PN_TABLE/wago.121808.pn',
    'NOUMS': '../PN_TABLE/pn.csv.m3.120408.trim'
}

mcb = MeCab.Tagger()


def set_dict():
    '''
    極性辞書を辞書に読み込む。
    '''
    pn_dict = {}

    # 日本語評価極性辞書（用言編）
    with open(pn_path['VERBS'], 'r') as f:
        for line in f.readlines():
            line = line.split('\t')
            word = line[1].replace(' ', '').replace('\n', '')
            value = score['POSI'] if 'ポジ' in line[0] else score['NEGA']
            pn_dict[word] = value

    # 日本語評価極性辞書（名詞編）
    with open(pn_path['NOUMS'], 'r') as f:
        for line in f.readlines():
            line = line.split('\t')
            word = line[0]
            if line[1] == 'p':
                value = score['POSI']
            elif line[1] == 'n':
                value = score['NEGA']
            else:
                value = score['EQUAL']
            pn_dict[word] = value

    return pn_dict


def get_nega_posi(text, pn_dict):
    '''
    辞書を指定して、ネガポジ判定を行う。
    '''
    # 形態素解析
    words = []
    lines = mcb.parse(text).split('\n')
    for line in lines:
        line = line.split('\t')
        if line[0] == 'EOS':
            break
        else:
            p = line[1].split(',')
            word_type = p[0]
            word = p[6] if p[6] in pn_dict.keys() else line[0]
            if word_type in {'形容詞', '動詞', '名詞', '副詞'}:
                words.append(word)

    # ネガポジ判定
    pn_score = 0
    for word in words:
        if word in pn_dict.keys():
            pn_score += pn_dict[word]

    return pn_score
