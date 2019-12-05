import MeCab
import sys


attrs = ['tags',        # 품사 태그
         'semantic',    # 의미 부류
         'has_jongsung',  # 종성 유무
         'read',        # 읽기
         'type',        # 타입
         'first_pos',   # 첫번째 품사
         'last_pos',    # 마지막 품사
         'original',    # 원형
         'indexed']     # 인덱스 표현


def parse(result, allattrs=False, join=False):
    def split(elem, join=False):
        if not elem: return ('', 'SY')
        s, t = elem.split('\t')
        if join:
            return s + '/' + t.split(',', 1)[0]
        else:
            return (s, t.split(',', 1)[0])

    return [split(elem, join=join) for elem in result.splitlines()[:-1]]

class mecab_:
    
#     def __init__(self, dicpath='/usr/local/lib/mecab/dic/mecab-ko-dic'):
#         self.dicpath = dicpath
#         try:
#             self.tagger = Tagger('-d %s' % dicpath)
#             self.tagset = utils.read_json('%s/data/tagset/mecab.json' % utils.installpath)
#         except RuntimeError:
#             raise Exception('The MeCab dictionary does not exist at "%s". Is the dictionary correctly installed?\nYou can also try entering the dictionary path when initializing the Mecab class: "Mecab(\'/some/dic/path\')"' % dicpath)
#         except NameError:
#             raise Exception('Install MeCab in order to use it: http://konlpy.org/en/latest/install/')

    def __init__(self):
        self.tagger = MeCab.Tagger()

    def pos(self, phrase, flatten=True, join=False):
        """POS tagger.
        :param flatten: If False, preserves eojeols.
        :param join: If True, returns joined sets of morph and tag.
        """

        if sys.version_info[0] < 3:
            phrase = phrase.encode('utf-8')
            if flatten:
                result = self.tagger.parse(phrase).decode('utf-8')
                return parse(result, join=join)
            else:
                return [parse(self.tagger.parse(eojeol).decode('utf-8'), join=join)
                        for eojeol in phrase.split()]
        else:
            if flatten:
                result = self.tagger.parse(phrase)
                return parse(result, join=join)
            else:
                return [parse(self.tagger.parse(eojeol), join=join)
                        for eojeol in phrase.split()]

    def morphs(self, phrase):
        """Parse phrase to morphemes."""
        return [s for s, t in self.pos(phrase)]
