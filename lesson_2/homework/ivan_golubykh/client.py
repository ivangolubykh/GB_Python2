#!/usr/bin/python3
# Клиент игры "Запоминалка"
import socket
import unittest
import datetime
__author__ = 'Иван Голубых'
HOST, PORT = 'localhost', 9999


def datetime_code(date):
    ''' На вход должен поступать объект datetime.datetime, при этом
    год должен быть от 2000-го до 2099-го.

    * Дата-время:

        * дата в 2 байта: |7 бит: год-2000|4 бита: месяц|5 бит: число|

        Так, дата 2017.04.01 будет закодирована 2 байтами: 0x2281
        (в двоичном виде: 0010001010000001)

        * количество секунд в течение дня от 00:00:00, записана в 3 байта.
    >>> datetime_code(datetime.datetime(2017, 4, 1, 5, 24, 15))
    b'"\\x81\\x00K\\xff'
    '''
    def err_datetime():
        raise 'Неверный формат даты-времени для кодирования!'

    try:
        year = date.year - 2000
        month = date.month
        day = date.day
        second = date.hour * 3600 + date.minute * 60 + date.second
    except Exception:
        err_date()
    if not (0 <= year <= 99):
        # Нельзя передавать 3005 год и т.п. даты - битов не хватит для
        # кодирования
        err_date()
    # Сначала кодирую год в первые 7 бит + еще 9 бит в запасе:
    date_bin = int(bin(year)[2:]+'000000000', 2)
    # Потом прибавляю к нему месяц число + еще 5 бита в запасе:
    date_bin += int(bin(month)[2:]+'00000', 2)
    # Потом прибавляю к нему день:
    date_bin += int(bin(day)[2:], 2)
    # преобразую в строку из нулей и единиц:
    date_bin = '{:0>16}'.format(bin(date_bin)[2:])
    # Кодирую секунды в 24 бита + еще 9 бит в запасе:
    second_bin = '{:0>24}'.format(bin(second)[2:])
    # Перевожу дату и секунды в байты:
    rez = bytes([int(date_bin[:8], 2),
                 int(date_bin[8:], 2),
                 int(second_bin[:8], 2),
                 int(second_bin[8:16], 2),
                 int(second_bin[16:], 2)
                 ])
    return rez


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

    datetime_01 = datetime.datetime(year=2017, month=4, day=1, hour=5,
                                    minute=24, second=15)
    datetime_code(datetime_01)
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
