#
# https://github.com/sh2mg136/python_word_finder.git
#
import re
from itertools import product, permutations, combinations, combinations_with_replacement, islice
from multiprocessing import Process, Queue, Pool, current_process, freeze_support


def is_english(s) -> bool:
    try:
        s.encode(encoding='utf-8').decode('ascii')
    except UnicodeDecodeError:
        return False
    else:
        return True


#
# MultiProcessing ver
class WordFinderBase(object):
    # WORDS_PATH_ENG = 'F:\\projects\\english-words\\words_alpha.txt'
    WORDS_PATH_ENG = 'F:\\projects\\english-words-3\\english3.txt'
    WORDS_PATH_RUS = 'F:\\projects\\russian-words\\russian.txt'
    MODE = "NONE"  # NONE | ENG | RUS
    WordMask = ""
    Permutations = []
    Combinations = []
    Products = []
    TOTAL_PAGES = 0
    Words = set()
    PAGE_SIZE = 5000
    WordChunks = set()  # [set() for _ in range(1)]

    #
    #
    @staticmethod
    def group_elements(lst, chunk_size):
        lst = iter(lst)
        return iter(lambda: tuple(islice(lst, chunk_size)), ())

    #
    #
    @staticmethod
    def create_mask(mask: str, letters: str) -> str:
        inner_mask = "^"
        cnt = 0
        for ch in mask:
            if ch == '*' or ch == '?':
                cnt += 1
            else:
                if cnt > 0:
                    inner_mask += "[" + letters + "]{" + str(cnt) + "}"
                    cnt = 0
                inner_mask += ch
        if cnt > 0:
            inner_mask += "[" + letters + "]{" + str(cnt) + "}"
        inner_mask += "$"
        return inner_mask

    #
    #
    def __init__(self, letters: str, mask: str, page_size: int = 5000):
        self.Letters = letters
        self.WordLength = len(mask)
        self.WordMask = self.create_mask(mask, letters)
        self.MODE = "RUS"
        if is_english(self.Letters) is True:
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
        self.Products = product(self.Letters, repeat=self.WordLength)

        first_letter = ""
        ch = ["*", "$", "?", "%", "-", "+", "!", "|"]

        if mask[0] is not None and mask[0] != "" and mask[0] not in ch:
            print(f"First letter: {mask[0]}")
            first_letter = mask[0]
            for w in self.wrd:
                if w.startswith(mask[0]):
                    self.Words.add(w)
        else:
            self.Words = self.wrd

        cnt = 0
        for w in self.Words:
            cnt += 1

        print(f"Total words amount: {cnt}")

        self.PAGE_SIZE = page_size
        self.TOTAL_PAGES = int(len(self.Words) / self.PAGE_SIZE) + 1
        self.WordChunks = [set() for _ in range(self.TOTAL_PAGES)]
        print('Page amount:', self.TOTAL_PAGES)
        page = 0
        all_wrds_list = list(self.Words)
        output = []
        for out in self.group_elements(all_wrds_list, self.PAGE_SIZE):
            output.append(out)
        # print(len(output))
        for sp in output:
            self.WordChunks[page] = set(sp)
            page += 1

        assert len(self.WordChunks) == self.TOTAL_PAGES

        s = 0
        for lst in self.WordChunks:
            s += len(lst)
        print(s)
        assert s > 10000, 'words error'

        some_word = "relax"  # 'apple'  # 'supper'

        if first_letter == "" or first_letter == some_word[0]:
            b = False
            page = -1
            for lst in self.WordChunks:
                if b is True:
                    break
                page += 1
                # print('Page %s = %s' % (page, len(lst)))
                for wr in lst:
                    if wr == some_word:
                        b = True
                        break
            print('Is word [%s] found -> %s (page %s)' % (some_word, b, page))
            assert b is True
            print(self.Letters)
            print(self.WordMask)
            b = False
            for wr in self.WordChunks[page]:
                if wr == some_word:
                    b = True
                    break
            assert b is True
            print('Yeah, it`s true! Word [%s] found on page %s' % (some_word, page))
        print()
        print(mask)
        print(self.WordMask)
        print("Base initialized")
        print()
