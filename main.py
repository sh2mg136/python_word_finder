import re
import time
import math
import logging
import logging.config
from itertools import product, permutations, combinations, combinations_with_replacement
import WordFinder

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


def load_words():
    words_path = ""
    if MODE == "ENG":
        words_path = WORDS_PATH_ENG
    elif MODE == "RUS":
        words_path = WORDS_PATH_RUS
    with open(words_path) as word_file:
        valid_words = set(word_file.read().split())
    return valid_words


def load_list():
    txt_file = open(WORDS_PATH_ENG, "r")
    file_content = txt_file.read()
    content_list = file_content.split()
    return content_list


def find_all_words(combs: permutations) -> list[str]:
    f_result = []
    words_count = 0
    for cm in combs:
        words_count += 1
        # if cnt % 10000 == 0 print(cnt)
        wrd = ""
        for s in cm:
            wrd += s
        # print(wrd)
        if wrd in english_words:
            f_result.append(wrd)
        # if wrd in words:
        #    found_words.append(wrd)
    return f_result


def find_all_words_mask(combs: permutations, mask: str) -> list[str]:
    f_result = []
    words_count = 0
    for cm in combs:
        words_count += 1
        wrd = "".join(cm)
        if re.search(mask, wrd) and wrd in english_words:
            f_result.append(wrd)
        # s2 = [s for s in english_words if re.search(mask, wrd)]
        # if len(s2) > 0: f_result.append(s2[0])
    return f_result


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


if __name__ == '__main__':
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
    input_chars = 'acdghijlmopqrsuwxyz'
    letters_amount = 5
    # mask = "^л\w{3}$"
    # mask = "^\w{" + str(letters_amount) + "}$"
    mask = "^cra\w{2}"
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
        # finder.WordLength = letters_amount
        # res = finder.find_all_words()
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
