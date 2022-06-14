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
class WordFinderMP(object):
    WORDS_PATH_ENG = 'F:\\projects\\english-words\\words_alpha.txt'
    WORDS_PATH_RUS = 'F:\\projects\\russian-words\\russian.txt'
    MODE = "NONE"  # NONE | ENG | RUS
    WordMask = ""
    Permutations = []
    Combinations = []
    Products = []
    WordChunks = [set() for _ in range(1)]
    TOTAL_PAGES = 0

    #
    #
    @staticmethod
    def group_elements(lst, chunk_size):
        lst = iter(lst)
        return iter(lambda: tuple(islice(lst, chunk_size)), ())

    #
    #
    def __init__(self, letters: str, word_len: int, mask: str):
        self.Letters = letters
        self.WordLength = word_len
        self.WordMask = mask
        self.MODE = "RUS"
        if is_english(self.Letters) is True:
            self.MODE = "ENG"
        words_path = ""
        if self.MODE == "ENG":
            words_path = self.WORDS_PATH_ENG
        elif self.MODE == "RUS":
            words_path = self.WORDS_PATH_RUS
        with open(words_path) as word_file:
            self.Words = set(word_file.read().split())
        self.Permutations = permutations(self.Letters, self.WordLength)
        self.Combinations = combinations_with_replacement(self.Letters, self.WordLength)
        self.Products = product(self.Letters, repeat=self.WordLength)

        PAGE_SIZE = 10000
        self.TOTAL_PAGES = int(len(self.Words) / PAGE_SIZE) + 1
        self.WordChunks = [set() for _ in range(self.TOTAL_PAGES)]
        print('Page amount:', self.TOTAL_PAGES)
        page = 0
        all_wrds_list = list(self.Words)
        output = []
        for out in self.group_elements(all_wrds_list, PAGE_SIZE):
            output.append(out)
        # print(len(output))
        for sp in output:
            self.WordChunks[page] = set(sp)
            page += 1

    #
    # Function used to calculate result
    def _calc(self, func, args) -> list[str]:
        result = func(*args)
        # return '%s says that %s%s = %s' % (current_process().name, func.__name__, args, result)
        # if len(result) <= 0: return None
        print('\t%s = %s' % (current_process().name, result))
        return result

    #
    # Function run by worker processes
    def _worker(self, inputs, output):
        for func, args in iter(inputs.get, 'STOP'):
            result = self._calc(func, args)
            output.put(result)

    #
    #
    def find_all_words_mask_rpt_mf(self, words: []) -> list[str]:
        f_result = []
        for cm in self.Products:
            wrd = "".join(cm)
            if re.search(self.WordMask, wrd) and wrd in words:
                f_result.append(wrd)
        return f_result

    #
    #
    def find(self) -> list[str]:
        NUMBER_OF_PROCESSES = 2
        TASKS = [(self.find_all_words_mask_rpt_mf, (self.WordChunks[i],)) for i in range(self.TOTAL_PAGES - 1)]
        # TASKS = [(mul, (i, 7)) for i in range(20)]

        task_queue = Queue()
        done_queue = Queue()

        for task in TASKS:
            task_queue.put(task)

        for i in range(NUMBER_OF_PROCESSES):
            Process(target=self._worker, args=(task_queue, done_queue)).start()

        answer = []

        # Get and print results
        print('Unordered results:')
        for i in range(len(TASKS)):
            res = done_queue.get()
            if res is not None and len(res) > 0:
                for wr in res:
                    answer.append(wr)

        # Tell child processes to stop
        for i in range(NUMBER_OF_PROCESSES):
            task_queue.put('STOP')

        return answer
