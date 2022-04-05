import re
from itertools import product, permutations, combinations, combinations_with_replacement


# class
class WordFinder(object):

    WORDS_PATH_ENG = 'F:\\projects\\english-words\\words_alpha.txt'
    WORDS_PATH_RUS = 'F:\\projects\\russian-words\\russian.txt'
    MODE = "NONE"

    #####################
    # assert not isEnglish('slabiky, ale liší se podle významu')
    # assert isEnglish('English')
    # assert not isEnglish('ގެ ފުރަތަމަ ދެ އަކުރު ކަ')
    # assert not isEnglish('how about this one : 通 asfަ')
    # assert isEnglish('?fd4))45s&')
    def is_english(self, s) -> bool:
        try:
            s.encode(encoding='utf-8').decode('ascii')
        except UnicodeDecodeError:
            return False
        else:
            return True

    #####################
    def __init__(self, letters: str, word_len: int):
        self.Letters = letters
        self.WordLength = word_len
        self.MODE = "RUS"
        if self.is_english(self.Letters) is True:
            # self.Letters.isalpha():
            self.MODE = "ENG"
        words_path = ""
        if self.MODE == "ENG":
            words_path = self.WORDS_PATH_ENG
        elif self.MODE == "RUS":
            words_path = self.WORDS_PATH_RUS
        with open(words_path) as word_file:
            self.Words = set(word_file.read().split())

    #####################
    def find_all_words_mask(self, mask: str) -> list[str]:
        combs = permutations(self.Letters, self.WordLength)
        f_result = []
        words_count = 0
        for cm in combs:
            words_count += 1
            wrd = "".join(cm)
            if re.search(mask, wrd) and wrd in self.Words:
                f_result.append(wrd)
        return f_result

    ######################
    def find_all_words(self) -> list[str]:
        combs = permutations(self.Letters, self.WordLength)
        f_result = []
        words_count = 0
        for cm in combs:
            words_count += 1
            wrd = "".join(cm)
            if wrd in self.Words:
                f_result.append(wrd)
            # if wrd in words:
            #    found_words.append(wrd)
        return f_result

