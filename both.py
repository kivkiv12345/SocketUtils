from multiprocessing import shared_memory, Manager, Process, Queue
import socket
from time import sleep
from random import randint

# We may use a shared list for increased flexibility.
#manager = Manager()
#shared_list = manager.list()


def server_append(queue:Queue):
    """ Receives data from the client, then appends it to the list. """
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
        sock.bind((socket.gethostname(), 9355))

        while True:  # Continue to receive data, until the user stops the program, or the socket times out.
            data, addr = sock.recvfrom(1024)
            print('Received some data')
            #shared_list.append(data.decode('utf-8'))
            _msg = data.decode('utf-8')
            for i in range(randint(2, 6)):
                queue.put(_msg * i)


def client_send(queue:Queue, server:Process):
    """ Sends data to the server which should be appended to the list. """
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as client_socket:
        i = 0
        while True:
            i += 1
            client_socket.sendto(input('provide input').encode('utf-8'), (socket.gethostname(), 9355))
            sleep(1)  # append to the list
            #print(shared_list)
            while not queue.empty():
                print(queue.get())
            if i == 3:
                print('closing server')
                server.terminate()


if __name__ == '__main__':

    shared_queue = Queue()

    server = Process(target=server_append, args=(shared_queue,))
    server.start()

    client_send(shared_queue, server)