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

WORDS_PATH_ENG = 'F:\\projects\\english-words\\words_alpha.txt'
WORDS_PATH_RUS = 'F:\\projects\\russian-words\\russian.txt'


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


def group_elements(lst, chunk_size):
    lst = iter(lst)
    return iter(lambda: tuple(islice(lst, chunk_size)), ())


#
def is_english(s) -> bool:
    try:
        s.encode(encoding='utf-8').decode('ascii')
    except UnicodeDecodeError:
        return False
    else:
        return True


#
#
def _find_all_words_mask_rpt_mf(products: set, words: set, word_len: int, mask: str) -> list[str]:
    f_result = []
    for cm in products:
        wrd = "".join(cm)
        if re.search(mask, wrd) and wrd in words:
            f_result.append(wrd)
    return f_result


#
#
def _find_all_words_mask(products, words, mask: str) -> list[str]:
    f_result = []
    for cm in products:
        wrd = "".join(cm)
        if re.search(mask, wrd) and wrd in words:
            print(wrd)
            f_result.append(wrd)
            # yield wrd
    return f_result


def f1(name: str, mask: str) -> str:
    re.compile(mask)
    if re.search(mask, name):
        print('Hello, %s  (%s)' % (name, current_thread().name))
        return name


result_list = []


def log_result(result):
    # This is called whenever foo_pool(i) returns a result.
    # result_list is modified only by the main process, not the pool workers.
    result_list.append(result)


#
#
def find(letters: str, word_len: int, mask: str) -> list[str]:
    Letters = letters
    WordLength = word_len
    WordMask = mask
    MODE = "RUS"
    if is_english(Letters) is True:
        MODE = "ENG"
    words_path = ""
    if MODE == "ENG":
        words_path = WORDS_PATH_ENG
    elif MODE == "RUS":
        words_path = WORDS_PATH_RUS
    with open(words_path) as word_file:
        Words = set(word_file.read().split())
    # Permutations = permutations(Letters, WordLength)
    # Combinations = combinations_with_replacement(Letters, WordLength)
    Products = product(Letters, repeat=WordLength)

    PAGE_SIZE = 10000
    TOTAL_PAGES = int(len(Words) / PAGE_SIZE) + 1
    assert TOTAL_PAGES > 0
    WordChunks = [set() for _ in range(TOTAL_PAGES)]
    print('Page amount:', TOTAL_PAGES)
    page = 0
    all_wrds_list = list(Words)
    output = []
    for out in group_elements(all_wrds_list, PAGE_SIZE):
        output.append(out)
    # print(len(output))
    for sp in output:
        WordChunks[page] = set(sp)
        page += 1

    assert len(WordChunks) == TOTAL_PAGES

    s = 0
    for lst in WordChunks:
        s += len(lst)
    print(s)
    assert s > 350000

    some_word = 'supper'
    b = False
    page = -1
    for lst in WordChunks:
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
    print(Letters)
    print(WordMask)
    b = False
    for wr in WordChunks[page]:
        if wr == some_word:
            b = True
            break
    assert b is True
    print('Yeah, it`s true! Word [%s] found on page %s' % (some_word, page))
    print()

    names = ['Max', 'Alyona', 'John', 'Michel', 'Bobby', 'Steven', 'Nikolas', 'Jason', 'Piter', 'Andy', 'Ilona']
    cnt = 0
    answer = []

    '''
    # METHOD 1
    task_queue = Queue()
    done_queue = Queue()
    NUMBER_OF_THREADS = 4
    # TASKS = [(self.find_all_words_mask_rpt_mf, (self.WordChunks[i],)) for i in range(self.TOTAL_PAGES - 1)]
    
    for x in range(NUMBER_OF_THREADS):
        worker = TaskWorker(task_queue, done_queue)
        worker.daemon = True
        worker.start()

    for dic in WordChunks:
        task_queue.put((_find_all_words_mask_rpt_mf, (cnt, Products, dic, WordLength, WordMask)), timeout=30)
        cnt += 1

    task_queue.join()

    print('Unordered results:')
    for i in range(NUMBER_OF_THREADS):
        res = done_queue.get()
        if res is not None and len(res) > 0:
            for wr in res:
                answer.append(wr)
    '''

    # METHOD 2
    with ThreadPool(processes=3) as pool:
        for dic in names:  # WordChunks:
            # pool.apply_async(_find_all_words_mask, (Products, dic, WordMask,), callback=log_result)
            # async_result = pool.apply_async(_find_all_words_mask, (cnt, Products, dic, WordLength, WordMask,))
            pool.apply_async(f1, (dic, "\w{5}"), callback=log_result)
            # answer.append(async_result.get())
            cnt += 1
        pool.close()
        pool.join()
        print(cnt)
        print(result_list)

    '''
    # METHOD 3
    with concurrent.futures.ThreadPoolExecutor(max_workers=3) as executor:
        future_to_url = {executor.submit(f1, name): name for name in names}
        for future in concurrent.futures.as_completed(future_to_url):
            name = future_to_url[future]
            try:
                data = future.result()
            except Exception as exc:
                print('%r generated an exception: %s' % (name, exc))
            else:
                print('%r page is %d bytes' % (name, len(data)))
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

    return answer
