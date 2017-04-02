#!/usr/bin/python3
# Сервер игры "Запоминалка"
import socketserver
import random
__author__ = 'Иван Голубых'
HOST, PORT = 'localhost', 9999


class MemTCPHandler(socketserver.BaseRequestHandler):

    def handle(self):
        # self.data = self.request.recv(1024).decode()
        self.data = self.request.recv(1024)
        print("Клиент {} сообщает {}".format(self.client_address[0],
                                             self.data))
        if self.data == b"Test":
            ''' Это для проведения unit-теста.
            '''
            self.request.sendall(bytes('Test=ok', 'utf-8'))
        elif self.data == b"I_WANNA_PLAY":
            nums = random.sample(range(1, 100), 18) * 2
            random.shuffle(nums)
            s_nums = [str(n) for n in nums]
            s_nums = ';'.join(s_nums)

            self.request.sendall(bytes('NUMS;'+s_nums, 'utf-8'))
        else:
            self.request.sendall(bytes('Байты получены.', 'utf-8'))
            print('Неизвестный запрос')


def main():
    server = socketserver.TCPServer((HOST, PORT), MemTCPHandler)
    print('Сервер игры запущен')
    server.serve_forever()


if __name__ == '__main__':
    main()
