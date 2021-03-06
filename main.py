# Chapter06/example8.py
from math import sqrt
import multiprocessing


class Worker(multiprocessing.Process):
    def __init__(self, que_in, que_out):
        super(Worker, self).__init__()
        self.que_in = que_in
        self.que_out = que_out

    def run(self):
        while True:
            pass



class Consumer(multiprocessing.Process):
    def __init__(self, task_queue, result_queue):
        multiprocessing.Process.__init__(self)
        self.task_queue = task_queue
        self.result_queue = result_queue

    def run(self):
        pname = self.name

        while True:
            temp_task = self.task_queue.get()

            if temp_task is None:
                print('Exiting %s...' % pname)
                self.task_queue.task_done()
                break

            print('%s processing task: %s' % (pname, temp_task))

            answer = temp_task.process()
            self.task_queue.task_done()
            self.result_queue.put(answer)


class Task():
    def __init__(self, x):
        self.x = x

    def process(self):
        if self.x < 2:
            return '%i is not a prime number.' % self.x

        if self.x == 2:
            return '%i is a prime number.' % self.x

        if self.x % 2 == 0:
            return '%i is not a prime number.' % self.x

        limit = int(sqrt(self.x)) + 1
        for i in range(3, limit, 2):
            if self.x % i == 0:
                return '%i is not a prime number.' % self.x

        return '%i is a prime number.' % self.x

    def __str__(self):
        return 'Checking if %i is a prime or not.' % self.x


# if __name__ == '__main__':
#     tasks = multiprocessing.JoinableQueue()
#     results = multiprocessing.Queue()
#
#     # spawning consumers with respect to the
#     # number cores available in the system
#     n_consumers = multiprocessing.cpu_count()
#     print('Spawning %i consumers...' % n_consumers)
#     consumers = [Consumer(tasks, results) for i in range(n_consumers)]
#     for consumer in consumers:
#         consumer.start()
#
#     # enqueueing jobs
#     my_input = [2, 36, 101, 193, 323, 513, 1327, 100000, 9999999, 433785907]
#     for item in my_input:
#         tasks.put(Task(item))
#
#     for i in range(n_consumers):
#         tasks.put(None)
#
#     tasks.join()
#
#     for i in range(len(my_input)):
#         temp_result = results.get()
#         print('Result:', temp_result)
#
#     print('Done.')

from glob import glob
import time
import signal


RUN = True


def handle(signum, frame):
    global RUN
    print("Получен сигнал завершения главного процесса.")
    RUN = False


signal.signal(signal.SIGINT, handle)

if __name__ == "__main__":
    # настройка очередй и процессов
    que_results = multiprocessing.Queue() # общая для всех очередь Результатов

    # создаем рабочих с количеством ядер доступных в системе
    n_workers = multiprocessing.cpu_count()

    print(f'Создание {n_workers} рабочих процессов...')

    workers = list()
    for i in range(n_workers):
        que_in = multiprocessing.JoinableQueue()
        worker = Worker(que_in, que_results)

        workers.append(worker)

    for worker in workers:
        worker.start()

    # запуск главного цикла
    print("{:-^50}".format("Мониторинг директории"))
    file_path = r"./test/*"
    files = dict()

    while RUN:
        dir_files = glob(file_path)
        new_files = []
        for file in dir_files:
            if file not in files:
                new_files.append(file)
                files[file] = 0

        if new_files:
            print("Найдено {} файла.".format(len(new_files)))
            print(*new_files, sep="\n")

        time.sleep(5)


