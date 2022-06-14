#
# https://github.com/sh2mg136/python_word_finder.git
#
import re
from itertools import product, permutations, combinations, combinations_with_replacement, islice
from queue import Queue
from threading import Thread, current_thread
from multiprocessing.pool import ThreadPool
import concurrent.futures
import urllib.request


URLS = ['http://www.foxnews.com/',
        'http://www.cnn.com/',
        'http://europe.wsj.com/',
        'http://www.bbc.co.uk/',
        'http://some-made-up-domain.com/']


# Retrieve a single page and report the URL and contents
def load_url(url, timeout):
    with urllib.request.urlopen(url, timeout=timeout) as conn:
        return conn.read()


#
def is_english(s) -> bool:
    try:
        s.encode(encoding='utf-8').decode('ascii')
    except UnicodeDecodeError:
        return False
    else:
        return True


class TaskWorker(Thread):

    def __init__(self, queue, done_queue):
        Thread.__init__(self)
        self.queue = queue
        self.done_queue = done_queue

    def _calc(self, func, args) -> list[str]:
        result = func(*args)
        # print('\t%s -> %s' % (current_thread(), result))
        return result

    def run(self):
        while True:
            func, args = self.queue.get()
            try:
                num, result = self._calc(func, args)
                print('\t%s : %s -> %s' % (num, current_thread().name, result))
                self.done_queue.put(result)
            finally:
                self.queue.task_done()


#
# MultiThreading ver
class WordFinderMTH(object):
    WORDS_PATH_ENG = 'F:\\projects\\english-words\\words_alpha.txt'
    WORDS_PATH_RUS = 'F:\\projects\\russian-words\\russian.txt'
    MODE = "NONE"  # NONE | ENG | RUS
    WordMask = ""
    Permutations = []
    Combinations = []
    Products = []
    WordChunks = [set() for _ in range(30)]
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
        assert self.TOTAL_PAGES > 0
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

        assert len(self.WordChunks) == self.TOTAL_PAGES

        s = 0
        for lst in self.WordChunks:
            s += len(lst)
        print(s)
        assert s > 350000

        some_word = 'supper'
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

    #
    #
    def _find_all_words_mask_rpt_mf(self, num: int, words: []) -> tuple[int, list[str]]:
        f_result = []
        for cm in self.Products:
            wrd = "".join(cm)
            if re.search(self.WordMask, wrd) and wrd in words:
                f_result.append(wrd)
        return num, f_result

    #
    #
    def _find_all_words_mask(self, num: int) -> list[str]:
        f_result = []
        for cm in self.Products:
            wrd = "".join(cm)
            if len(wrd) == self.WordLength \
                    and re.search(self.WordMask, wrd) \
                    and wrd in self.WordChunks[num]:
                f_result.append(wrd)
        return f_result

    #
    #
    def find(self) -> list[str]:
        task_queue = Queue()
        done_queue = Queue()
        NUMBER_OF_THREADS = 4
        # TASKS = [(self.find_all_words_mask_rpt_mf, (self.WordChunks[i],)) for i in range(self.TOTAL_PAGES - 1)]
        cnt = 0
        answer = []

        for x in range(NUMBER_OF_THREADS):
            worker = TaskWorker(task_queue, done_queue)
            worker.daemon = True
            worker.start()
       
        for dic in self.WordChunks:
            task_queue.put((self._find_all_words_mask_rpt_mf, (cnt, dic,)), timeout=20)
            cnt += 1

        task_queue.join()

        '''
        pool = ThreadPool(processes=4)
        for x in range(self.TOTAL_PAGES):
            async_result = pool.apply_async(self._find_all_words_mask, (x,))  # tuple of args for foo
            answer += async_result.get()
            cnt += 1
        '''

        '''
        with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
            # Start the load operations and mark each future with its URL
            future_to_url = {executor.submit(load_url, url, 60): url for url in URLS}
            for future in concurrent.futures.as_completed(future_to_url):
                url = future_to_url[future]
                try:
                    data = future.result()
                except Exception as exc:
                    print('%r generated an exception: %s' % (url, exc))
                else:
                    print('%r page is %d bytes' % (url, len(data)))
        '''

        '''    
        with concurrent.futures.ThreadPoolExecutor(max_workers=NUMBER_OF_THREADS) as executor:
            tasks = {executor.submit(self._find_all_words_mask, x): x for x in range(self.TOTAL_PAGES)}
            print(len(tasks))
            for future in concurrent.futures.as_completed(tasks, timeout=30):
                cur = tasks[future]
                try:
                    data = future.result()
                    # answer += data
                except Exception as ex:
                    print('%r generated an exception: %s' % (cur, ex))
                else:
                    answer += data
                    print('%s page is %d words' % (cur, len(data)))
        '''

        '''
        print('Unordered results:')
        for i in range(NUMBER_OF_THREADS):
            res = done_queue.get()
            if res is not None and len(res) > 0:
                for wr in res:
                    answer.append(wr)
        '''
        return answer
