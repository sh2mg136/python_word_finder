#
# https://github.com/sh2mg136/python_word_finder.git
#
import re
from itertools import product, permutations, combinations, combinations_with_replacement, islice
from threading import Thread
# from queue import Queue
from multiprocessing import Process, Queue, Pool, current_process, freeze_support


#
# create regex mask from [*pp**] to [\w{1}pp\w{2}]
def create_mask(mask: str, letters: str) -> str:
    inner_mask = "^"
    cnt = 0
    for ch in mask:
        if ch == '*' or ch == '?':
            cnt += 1
        else:
            if cnt > 0:
                # inner_mask += "\\w{"+str(cnt)+"}"
                inner_mask += "[" + letters + "]{" + str(cnt) + "}"
                cnt = 0
            inner_mask += ch
    if cnt > 0:
        # inner_mask += "\\w{" + str(cnt) + "}"
        # inner_mask += "[a-z]{" + str(cnt) + "}"
        inner_mask += "[" + letters + "]{" + str(cnt) + "}"
    inner_mask += "$"
    return inner_mask


class WordFinder(object):

    # https://github.com/dwyl/english-words.git
    WORDS_PATH_ENG = 'F:\\projects\\english-words\\words_alpha.txt'
    # https://github.com/danakt/russian-words.git
    WORDS_PATH_RUS = 'F:\\projects\\russian-words\\russian.txt'
    MODE = "NONE"  # NONE | ENG | RUS

    WordMask = ""
    Permutations = []
    Combinations = []
    Words = set()

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
    def __init__(self, letters: str, mask: str = "*"):
        self.Letters = letters
        self.WordLength = len(mask)
        self.WordMask = create_mask(mask, letters)
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
            # self.Words = set(word_file.read().split())
            self.wrd = set(word_file.read().split())

        self.Permutations = permutations(self.Letters, self.WordLength)
        self.Combinations = combinations_with_replacement(self.Letters, self.WordLength)

        ch = ["*", "$", "?", "%", "-", "+", "!", "|"]

        if mask[0] is not None and mask[0] != "" and mask[0] not in ch:
            print(f"First letter: {mask[0]}")
            for w in self.wrd:
                if w.startswith(mask[0]):
                    self.Words.add(w)
        else:
            self.Words = set(self.wrd)

        cnt = 0
        for w in self.Words:
            cnt += 1

        print(f"is set: {type(self.Words) is set}")
        print(f"is list: {type(self.Words) is list}")
        print(f"Total words amount: {cnt}")
        print(mask)
        print(self.WordMask)
        print("Initialized")
        print()

    #####################
    def find_all_words_mask(self) -> list[str]:
        combs = permutations(self.Letters, self.WordLength)
        f_result = []
        words_count = 0
        for cm in combs:
            words_count += 1
            wrd = "".join(cm)
            if re.search(self.WordMask, wrd) and wrd in self.Words:
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

    #####################
    def find_all_words_mask_rpt(self) -> list[str]:
        combs = combinations_with_replacement(self.Letters, self.WordLength)
        f_result = []
        for cm in combs:
            wrd = "".join(cm)
            if re.search(self.WordMask, wrd) and wrd in self.Words:
                f_result.append(wrd)
        return f_result

    ######################
    def find_all_words_mf(self, words) -> list[str]:
        f_result = []
        words_count = 0
        for cm in self.Permutations:
            words_count += 1
            wrd = "".join(cm)
            if wrd in words:
                f_result.append(wrd)
        return f_result

    #####################
    def find_all_words_mask_rpt_mf(self, words: []) -> list[str]:
        f_result = []
        for cm in self.Combinations:
            wrd = "".join(cm)
            if re.search(self.WordMask, wrd) and wrd in words:
                f_result.append(wrd)
        return f_result

