import random
import re
import time
import math
import logging
import logging.config
from itertools import product, permutations, combinations, combinations_with_replacement, islice, zip_longest
import WordFinder
from multiprocessing import Process, Queue, Pool, current_process, freeze_support
from threading import Thread
from concurrent.futures import ThreadPoolExecutor
from functools import partial
# from time import time
import numpy as np
# from queue import Queue


# logging.basicConfig(level=logging.DEBUG)
# logging.basicConfig(format='%(process)d-%(levelname)s-%(message)s')
logging.config.fileConfig(fname='log.conf', disable_existing_loggers=False)
logger = logging.getLogger(__name__)
# logger = logging.getLogger('fHandler')

f_handler = logging.FileHandler('file.log')
f_handler.setLevel(logging.INFO)
f_format = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
f_handler.setFormatter(f_format)
logger.addHandler(f_handler)

WORDS_PATH_ENG = 'F:\\projects\\english-words\\words_alpha.txt'
WORDS_PATH_RUS = 'F:\\projects\\russian-words\\russian.txt'
MODES = ["ENG", "RUS"]
MODE = "ENG"

PATHS_ENG = [
    'F:\\projects\\english-words-2\\words_1.txt',
    'F:\\projects\\english-words-2\\words_2.txt',
    'F:\\projects\\english-words-2\\words_3.txt',
    'F:\\projects\\english-words-2\\words_4.txt',
    'F:\\projects\\english-words-2\\words_5.txt',
]


def load_words():
    words_path = ""
    if MODE == "ENG":
        words_path = WORDS_PATH_ENG
    elif MODE == "RUS":
        words_path = WORDS_PATH_RUS
    with open(words_path) as word_file:
        valid_words = set(word_file.read().split())
    return valid_words


def load_words_2():
    words = [set() for _ in range(5)]
    i = 0
    for pth in PATHS_ENG:
        with open(pth) as word_file:
            words[i] = set(word_file.read().split())
            i += 1
    return words


def load_list():
    txt_file = open(WORDS_PATH_ENG, "r")
    file_content = txt_file.read()
    content_list = file_content.split()
    return content_list


def test_func_01(eng_words: set):
    # type
    print(type(eng_words) is list)
    print(type(eng_words) is dict)
    print(type(eng_words) is set)
    print(type(eng_words) is str)
    print("---")
    # demo print
    print('fate' in eng_words)
    print(eng_words.pop())
    print(eng_words.pop())
    print("---")
    print(len(eng_words))
    print("---")
    a = {1, 2, 3, 30, 40, 300}
    b = {10, 20, 30, 40}
    a2 = a.difference(b)
    b2 = b.difference(a)
    print(a2)
    print(b2)
    print("---")
    words = load_list()
    print(words[123456])
    print("---")
    # str_match = [s for s in words if "ack" in s]
    str_match = [s for s in words if "gate" in s and len(s) in [4, 5]]
    print(str_match)
    print("---")
    # sss = re.search("break(.?)(.?)st", words[123])
    sss = [s for s in words if re.search("^break(.?)(.?)st$", s)]
    print(sss)
    print('race' in words)
    print("---")


def group_elements(lst, chunk_size):
    lst = iter(lst)
    return iter(lambda: tuple(islice(lst, chunk_size)), ())


def group_elements_2(n, iterable, padvalue=''):
    return zip_longest(*[iter(iterable)] * n, fillvalue=padvalue)


def group_elements_3(n, iterable):
    return zip_longest(*[iter(iterable)] * n)


def group_elements_4(lst: list, page_size: int):
    return lambda tmp_lst, p_size: [lst[ii:ii + page_size] for ii in range(0, len(lst), page_size)]


def print_name(name):
    print('Hello, ', name)


#
# Function run by worker processes
#
def worker(input, output):
    for func, args in iter(input.get, 'STOP'):
        result = calculate(func, args)
        output.put(result)


#
# Function used to calculate result
#
def calculate(func, args):
    result = func(*args)
    # return '%s says that %s%s = %s' % (current_process().name, func.__name__, args, result)
    # if len(result) <= 0: return None
    return '%s = %s' % (current_process().name, result)


def mul(a, b):
    # time.sleep(0.5 * random.random())
    return a * b


def find_all_words_mask_rpt_mf(words: [], products: [], mask: str) -> list[str]:
    f_result = []
    for cm in products:
        wrd = "".join(cm)
        if re.search(mask, wrd) and wrd in words:
            f_result.append(wrd)
    return f_result


def experiment2():
    ts = time.time()
    finder = WordFinder.WordFinder2("acdefhiklrstnop", 7, "^d[a-z]{1}ari[a-z]{2}$")
    # finder = WordFinder.WordFinder2("acdefhiklrstnop", 6, "[a-z]{2}pp[a-z]{2}")
    # finder = WordFinder.WordFinder2("acdefhiklrstnop", 5, "^app[a-z]{2}")
    print('Took %s' % (time.time() - ts))
    ts = time.time()
    res = finder.find()
    print(">>> RESULT >>>")
    print(res)
    print('Took %s' % (time.time() - ts))


def experiment():
    # finder = WordFinder.WordFinder("abcple", 5)
    # res = finder.find_all_words_mask_rpt("^a\\w{2}le$")
    # print(res)

    test_list = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10']
    for output in group_elements(test_list, 3):
        print(output)

    ts = time.time()
    all_wrds = load_words()
    all_wrd_cnt = len(all_wrds)
    print(all_wrd_cnt)
    PAGE_SIZE = 4000
    total_pages = int(len(all_wrds) / PAGE_SIZE) + 1
    wrds = [set() for _ in range(total_pages)]
    print('Page amount:', total_pages)
    page = 0
    all_wrds_list = list(all_wrds)

    '''
    for output in group_elements(all_wrds_list, page_size):
        wrds[page] = set(output)
        page += 1
        # print(output)
    '''

    # sp = group_elements_4(all_wrds_list, page_size)
    # output = sp(all_wrds_list, page_size)
    output = []
    for out in group_elements(all_wrds_list, PAGE_SIZE):
        output.append(out)

    print(len(output))
    # print(output[0])
    for sp in output:
        wrds[page] = set(sp)
        page += 1

    # wrds = load_words_2()
    # pages = len(wrds)
    # print(pages)

    # final_list = lambda all_wrds, page_size: [all_wrds[ii:ii + page_size] for ii in range(0, len(all_wrds), page_size)]
    # wrds = final_list(all_wrds, page_size)
    # for new_list in group_elements(all_wrds, page_size): wrds.append(new_list)
    # wrds = group_elements(all_wrds, page_size)
    # wrds = [all_wrds[i:i + page_size] for i in range(0, len(all_wrds), page_size)]
    # wrds = all_wrds.__sub__(1000)
    # wrds = np.array_split(all_wrds, page_size)

    # rnd_word = wrds[0].pop()
    # print(rnd_word)
    # rnd_word = wrds[pages-1].pop()
    # print(rnd_word)

    print('Max page number: ', page)
    '''
    if page > 0:
        for i in range(page):
            rnd_word = wrds[i].pop()
            print(rnd_word)
    '''
    print('Took %s', time.time() - ts)

    # wrds = load_words_2()
    # finder = WordFinder.WordFinder("apbcelipmnop", 5, "^a\w{4}")

    b = False
    s = 0
    for lst in wrds:
        s += len(lst)
        # print(len(lst))
        for wr in lst:
            if wr == 'apple':
                b = True
                break
    print(s)
    print(b)

    ts = time.time()
    # zootic
    # finder2 = WordFinder.WordFinder2("aceiklmnopztx", 6, "zoo[a-z]{3}")
    # pineaPPle
    # finder2 = WordFinder.WordFinder2("acdefhiklnop", 9, "[a-z]{5}pp[a-z]{2}")
    # diarist
    finder2 = WordFinder.WordFinder2("acdefhiklrstnop", 7, "[a-z]{2}ari[a-z]{2}")
    print('Took %s', time.time() - ts)
    answer = []
    res = []
    answers_count = 0
    print('Word`s sets count:', len(wrds))
    print('Words in set #0:', len(wrds[0]))
    print('total_pages:', total_pages)

    NUMBER_OF_PROCESSES = 2
    TASKS = [(find_all_words_mask_rpt_mf, (wrds[i], finder2.Products, finder2.WordMask)) for i in range(total_pages-1)]
    # TASKS = [(mul, (i, 7)) for i in range(20)]

    task_queue = Queue()
    done_queue = Queue()

    for task in TASKS:
        task_queue.put(task)

    for i in range(NUMBER_OF_PROCESSES):
        Process(target=worker, args=(task_queue, done_queue)).start()

    # Get and print results
    print('Unordered results:')
    for i in range(len(TASKS)):
        res = done_queue.get()
        # if res is not None and len(res) > 0:
        if res is not None:
            print('\t', res)
        # print('\t', done_queue.get())

    # Tell child processes to stop
    for i in range(NUMBER_OF_PROCESSES):
        task_queue.put('STOP')

    print('Process complete! Took', time.time() - ts)

    '''
    with Pool(4) as thread_pool:
        # res = [pool.apply_async(calculate, t) for t in TASKS]
        res.append(thread_pool.map(finder2.find_all_words_mask_rpt_mf, wrds))
        # res = thread_pool.map(finder2.find_all_words_mask_rpt_mf, wrds)
        # answer.append(res)
        for r in res:
            if len(r) > 0:
                for a in r:
                    answers_count += 1
                    answer.append(a)
                # print(r)

    print('Found:', answers_count)
    print(answer)

    print('Pool complete! Took', time() - ts)
    '''

    # queue = Queue()

    '''
    res = []
    ts = time()
    # finder2 = WordFinder.WordFinder2("abcdefghijklmnopq", 9, "[a-z]{5}pp[a-z]{2}")
    # finder2 = WordFinder.WordFinder2("acdefiklmnop", 5, "[a-z]{1}pp[a-z]{2}")
    with ThreadPoolExecutor(4) as executor:
        fn = partial(finder2.find_all_words_mask_rpt_mf)
        res += executor.map(fn, wrds, timeout=30)
    print(res)
    print('Took %s', time() - ts)
    '''


def main():
    start = time.time()
    english_words = load_words()
    # test_func_01(english_words)
    # comb = permutations('ABCD', 4)
    # comb = permutations('pleapeinp', 9)
    #########################################
    # input_chars = 'летопись'
    # input_chars = 'bush'
    # input_chars = 'abcdefgijkmnopqrtuvxyz'
    # input_chars = 'etuqwifgjlzxvm'
    # finder = WordFinder.WordFinder2("acdefhiklrstnop", 7, "^d[a-z]{1}ari[a-z]{2}$")
    input_chars = 'acdefhiklrstni'
    letters_amount = 7
    # mask = "^л\w{3}$"
    # mask = "^\w{" + str(letters_amount) + "}$"
    # mask = "^\w{9}$"
    mask = "^d[a-z]{1}ari[a-z]{2}$"
    #########################################

    finder = WordFinder.WordFinder(input_chars, letters_amount)
    try:
        logger.info(f"Find in symbols [{input_chars}], word len = {letters_amount}. mask = {mask}")
        print(f"Mode: {finder.MODE}")
        print("STEP 1")
        res = finder.find_all_words_mask(mask)
        print(res)
        print(f"Found count: {len(res)}")
        print("STEP 2")
        finder.WordLength = letters_amount
        res = finder.find_all_words()
        print(res)
        print(f"Found count: {len(res)}")
        a1 = 5
        a2 = 0
        # a3 = a1/a2
    except ValueError as err:
        logger.error(err)
        print("Could not convert data.")
    except (RuntimeError, UnboundLocalError) as err:
        logger.error(err)
        print(f"Some error occurred. {err}")
    except ZeroDivisionError as err:
        logger.error(err)
        print('Handling run-time error:', err)
    except BaseException as err:
        logger.error(err)
        print(f"Unexpected {err=}, {type(err)=}")

    # logger.info("Get permutations for: " + input_chars)
    # comb = permutations(input_chars, letters_amount)
    # start = time.time()
    # found_words = find_all_words(comb)
    # cnt = len(found_words)
    # print(f"Total count: {cnt}")
    # print(f"Found count: {len(found_words)}")
    # print(found_words)
    # print("---")
    # comb2 = permutations(input_chars, letters_amount)
    # fw2 = find_all_words_mask(comb2, '^g\w{4}$')
    # fw2 = find_all_words_mask(comb2, 'd\w{7}$')
    # print(f"Found count: {len(fw2)}")
    # print(fw2)
    end = time.time()
    print(f"Elapsed time: {round(end - start, 4)} sec")


if __name__ == '__main__':
    main()
    # freeze_support()
    # experiment()
    # experiment2()
