#
# https://github.com/sh2mg136/python_word_finder.git
#
import re
from multiprocessing import Process, Queue, Pool, current_process, freeze_support
import WordFinderBase


#
# MultiProcessing ver
class WordFinderMultiProc(WordFinderBase.WordFinderBase):
    def __init__(self, letters: str, mask: str, page_size: int = 5000):
        WordFinderBase.WordFinderBase.__init__(self, letters, mask, page_size)
        print("WordFinderMultiProc initialized")

    # Function used to calculate result
    def _calc(self, func, args) -> list[str]:
        result = func(*args)
        # return '%s says that %s%s = %s' % (current_process().name, func.__name__, args, result)
        # if len(result) <= 0: return None
        print('\t%s = %s' % (current_process().name, result))
        return result

    # Function run by worker processes
    def _worker(self, inputs, output):
        for func, args in iter(inputs.get, 'STOP'):
            result = self._calc(func, args)
            output.put(result)

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
