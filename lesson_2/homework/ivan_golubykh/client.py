#!/usr/bin/python3
# Клиент игры "Запоминалка"
import socket
import unittest
__author__ = 'Иван Голубых'
HOST, PORT = 'localhost', 9999


def send_string(string):
    print('Отправляются данные: \'{}\''.format(string))
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((HOST, PORT))
    sock.sendall(bytes(string, 'utf-8'))
    recvd = str(sock.recv(1024), 'utf-8')
    sock.close()
    print('Получен ответ:', recvd)
    return recvd


def main():

    send_string('I_WANNA_PLAY')
    send_string('test')
    send_string('Test')
    # __add__  ->  +


class TestThis(unittest.TestCase):
    def test_calc_hash_md5(self):
        from multiprocessing import Process  # Для многопоточных процессов
        import server  # загружаю библиотеку сервера из server.py
        import time
        # Создаю поток с функцией сервера
        server_process = Process(target=server.main)
        # Запускаю сервер в отдельном потоке
        server_process.start()
        time.sleep(2)  # Иначе сервер не успевает загрузиться
        rez = send_string('Test')
        # убиваю/завершаю сервер:
        server_process.terminate()
        server_process.join()  # Чтобы мёртвый процесс не висел в системе.
        self.assertEqual(rez, 'Test=ok')


if __name__ == '__main__':
    main()
