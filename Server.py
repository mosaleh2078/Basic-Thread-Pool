import time
import queue
import requests
import colorama
import typing as T
from socket import *
from threading import Thread, current_thread

CALLBACK = T.Callable[[str], str]
TASK = T.Tuple[CALLBACK, socket]
TASKQUEUE = queue.Queue
SERVERPORT = "Port#"
API_KEY = "<API-KEY>"

class Worker(Thread):
    def __init__(self, tasks: queue.Queue[TASK]):
        super().__init__()
        self.tasks = tasks

    def run(self) -> None:
        while True:
            func, connection = self.tasks.get()
            try:
                result = func(connection.recv(1024).decode())
            except Exception as err:
                raise err
            else:
                self.tasks.task_done()
                connection.send(result.encode())
                connection.close()

class ThreadPool:
    def __init__(self, num_threads:int):
        self.tasks: TASKQUEUE = queue.Queue(num_threads)
        self.num_threads = num_threads

        for _ in range(num_threads):
            worker = Worker(self.tasks)
            worker.daemon = True
            worker.start()

    def submit(self, func: CALLBACK, connection: socket) -> None:
        self.tasks.put((func, connection))

    def wait(self) -> None:
        self.tasks.join()

def get_price(currency:str) -> str:
    print(f"[{colorama.Fore.GREEN}+{colorama.Fore.RESET} Thread {current_thread().name} is responding")
    time.sleep(1)
    url: str = f"https://v6.exchangerate-api.com/v6/{API_KEY}/latest/{currency}"
    response = requests.get(url)
    data = response.json()
    if response.status_code == 200:
        return f"1 {currency} equals {data['conversion_rates']['IRR']} Iranian Rials"
    else:
        print(f"Error: {data['error-type']}")

def main() -> None:
    pool = ThreadPool(num_threads=2)
    server_socket = socket(AF_INET, SOCK_STREAM)
    server_socket.bind(('', SERVERPORT))
    server_socket.listen(100)
    print(f"[{colorama.Fore.GREEN}+{colorama.Fore.RESET}] The server is ready to receive ...")
    while True:
        connection_socket, addr = server_socket.accept()
        pool.submit(get_price, connection_socket)

if __name__ == '__main__':
    main()
