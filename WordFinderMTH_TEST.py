#
# https://github.com/sh2mg136/python_word_finder.git
#
import multiprocessing
import asyncio
import re
from itertools import product, permutations, combinations, combinations_with_replacement, islice
from queue import Queue
from threading import Thread, current_thread
from multiprocessing.pool import ThreadPool
import concurrent.futures
import urllib.request
import time


class TaskWorker(Thread):

    def __init__(self, queue, done_queue):
        Thread.__init__(self)
        self.queue = queue
        self.done_queue = done_queue

    @staticmethod
    def _calc(func, args) -> list[str]:
        result = func(*args)
        # print('\t%s -> %s' % (current_thread(), result))
        return result

    def run(self):
        while True:
            func, args = self.queue.get()
            try:
                result = TaskWorker._calc(func, args)
                self.done_queue.put(result)
                print('\t%s -> %s' % (current_thread().name, result))
            finally:
                self.queue.task_done()


#
# MultiThreading ver
class WordFinder(object):
    WordMask = ""
    Permutations = []
    Combinations = []
    Products = []
    WordsList = [
        ['taxon', 'taxonomy', 'taxonomic', 'taxonomical', 'taxonomically', 'taxonomies', 'taxonomist', 'taxons',
         'taxor', 'taxpaid', 'taxpayer', 'taxpayers', 'taxpaying', 'taxus', 'taxwax', 'taxwise', 'tazza', 'tazzas',
         'tazze', 'tea', 'teaput'],
        ['teaberry', 'teaberries', 'teaboard', 'teaboards', 'teaboy', 'teabowl', 'teabowls', 'teabox', 'teaboxes',
         'teacake', 'teacart', 'teacarts', 'teach', 'teachability', 'teachable', 'teachableness', 'teachably'],
        ['teache', 'teached', 'teacher', 'teacherage', 'teacherdom', 'teacheress', 'teacherhood'],
        ['teachery', 'teacherish', 'teacherless',    'teacherly', 'teacherlike', 'teachers', 'teachership',
         'teaches', 'teachy', 'teaching', 'teachingly', 'teachings', 'teachless', 'teachment', 'teacup', 'teacupful'],
        ['teacupfuls', 'teacups', 'teacupsful', 'tead', 'teadish', 'teaey', 'teaer', 'teagardeny', 'teagle', 'teague',
         'teagueland', 'teaguelander', 'teahouse', 'teahouses', 'teaing', 'teaish', 'teaism', 'teak', 'teakettle',
         'teakettles', 'teaks', 'teakwood', 'teakwoods', 'teal', 'tealeafy', 'tealery'],
        ['tealess', 'teallite', 'teals', 'team', 'teamaker', 'teamakers', 'teamaking', 'teaman', 'teamed',
         'teameo', 'teamer', 'teaming', 'teamland', 'teamless', 'teamman', 'teammate', 'teammates', 'teams',
         'teamsman', 'teamster', 'teamsters','teamwise', 'teamwork', 'teamworks', 'tean', 'teanal', 'teap',
         'teapoy', 'teapoys', 'teapot', 'teapotful', 'teapots', 'teapottykin', 'tear', 'tearable', 'tearableness',
         'tearably', 'tearage', 'tearcat', 'teardown'],
        ['teardowns', 'teardrop', 'teardrops', 'teared', 'tearer', 'tearers', 'tearful', 'tearfully', 'tearfulness',
         'teargas', 'teargases', 'teapot', 'potter', 'sun', 'flower']
    ]
    TOTAL_PAGES = len(WordsList)
    print(len(WordsList))
    WordChunks = [set() for _ in range(TOTAL_PAGES)]
    result_list = []

    #
    def _check_word(self, word: str) -> tuple[bool, bool]:
        b = False
        page = -1
        for lst in self.WordChunks:
            if b is True:
                break
            page += 1
            # print('Page %s = %s' % (page, len(lst)))
            if word in lst:
                b = True
                break
        if b:
            print('Is word [%s] found -> %s (page %s)' % (word, b, page))
        b2 = word in self.WordChunks[page]
        if b2:
            print('Yeah, it`s true! Word [%s] found on page %s' % (word, page))
        return b, b2

    #
    def __init__(self, letters: str, word_len: int, mask: str):
        self.Letters = letters
        self.WordLength = word_len
        self.WordMask = mask
        self.Permutations = permutations(self.Letters, self.WordLength)
        self.Combinations = combinations_with_replacement(self.Letters, self.WordLength)
        self.Products = product(self.Letters, repeat=self.WordLength)

        self.TOTAL_PAGES = len(self.WordsList)
        assert self.TOTAL_PAGES > 0
        self.WordChunks = [set() for _ in range(self.TOTAL_PAGES)]
        print('Page amount:', self.TOTAL_PAGES)
        page = 0
        for sp in self.WordsList:
            self.WordChunks[page] = set(sp)
            page += 1

        assert len(self.WordChunks) == self.TOTAL_PAGES

        s = 0
        for lst in self.WordChunks:
            s += len(lst)
        print(s)
        assert s > 100

        print(self.Letters)
        print(self.WordMask)

        b1, b2 = self._check_word('teahouse')
        assert b1 is True
        assert b2 is True
        b1, b2 = self._check_word('teapot')
        assert b1 is True
        assert b2 is True
        print()

    #
    #
    def _find_all_words_mask_rpt(self, words: set) -> list[str]:
        f_result = []
        re.compile(self.WordMask)
        for cm in self.Products:
            wrd = "".join(cm)
            if re.search(self.WordMask, wrd) and wrd in words:
                f_result.append(wrd)
        return f_result

    #
    #
    def _find_all_words_mask(self, chunk_number: int) -> list[str]:
        f_result = []
        pat = re.compile(self.WordMask)
        for cm in self.Products:
            wrd = "".join(cm)
            # if len(wrd) == self.WordLength \
            if wrd in self.WordChunks[chunk_number] and pat.search(wrd):
                f_result.append(wrd)
        return f_result

    #
    #
    def log_result(self, result):
        # This is called whenever foo_pool(i) returns a result.
        # result_list is modified only by the main process, not the pool workers.
        if not self.result_list.__contains__(result):
            self.result_list.append(result)

    #
    #
    def find(self) -> list[str]:
        task_queue = Queue()
        done_queue = Queue()
        NUMBER_OF_THREADS = 3
        cnt = 0
        answer = []

        '''
        for x in range(NUMBER_OF_THREADS):
            worker = TaskWorker(task_queue, done_queue)
            worker.daemon = True
            worker.start()
       
        for dic in self.WordChunks:
            # task_queue.put((self._find_all_words_mask_rpt_mf, (dic,)), timeout=20)
            task_queue.put((self._find_all_words_mask, (cnt,)), timeout=10)
            cnt += 1

        task_queue.join()

        for i in range(NUMBER_OF_THREADS):
            res = done_queue.get()
            if res is not None and len(res) > 0:
                for wr in res:
                    if not answer.__contains__(wr):
                        answer.append(wr)
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

        def done_callback(res):
            result = res.result()
            for wrd in result:
                if not self.result_list.__contains__(wrd):
                    print(wrd)
                    self.result_list.append(wrd)

        with concurrent.futures.ThreadPoolExecutor(max_workers=NUMBER_OF_THREADS) as executor:
            tasks = {executor.submit(self._find_all_words_mask, x): x for x in range(self.TOTAL_PAGES)}
            for future in concurrent.futures.as_completed(tasks, timeout=30):
                cur = tasks[future]
                # future.add_done_callback(done_callback)
                try:
                    data = future.result()
                except Exception as ex:
                    print('%r generated an exception: %s' % (cur, ex))
                else:
                    for w in data:
                        if not answer.__contains__(w):
                            answer.append(w)

        # print(self.result_list)
        return answer

    #
    # Using  multiprocessing.Pool.apply_async
    def find_ver_2(self) -> list[str]:
        NUMBER_OF_THREADS = 3
        answer = []
        # pool = ThreadPool(processes=4)
        with multiprocessing.Pool(NUMBER_OF_THREADS) as pool:
            for x in range(self.TOTAL_PAGES):
                # for x in self.WordChunks:
                # async_result = pool.apply_async(self._find_all_words_mask, (x, ), callback=self.log_result)
                # async_result = pool.apply_async(self._find_all_words_mask_rpt, (x, ), callback=self.log_result)
                # pool.apply_async(self._find_all_words_mask_rpt, (x, ), callback=self.log_result)
                pool.apply_async(self._find_all_words_mask, (x,), callback=self.log_result)
                '''
                res = async_result.get()
                for w in res:
                    if not answer.__contains__(w):
                        answer.append(w)
                cnt += 1
                '''
            pool.close()
            pool.join()
            # print(self.result_list)
            for ww in self.result_list:
                for w in ww:
                    if not answer.__contains__(w):
                        answer.append(w)

        return answer

