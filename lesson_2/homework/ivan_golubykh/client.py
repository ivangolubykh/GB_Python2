#!/usr/bin/python3
# Клиент игры "Запоминалка"
import socket
import unittest
import datetime
__author__ = 'Иван Голубых'
HOST, PORT = 'localhost', 9999


class Tranzactions:
    '''  Класс для хранения и кодирования данных о транзакции
    '''
    def __init__(self):
        pass

    @staticmethod
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

    @staticmethod
    def tranz_code(tranz_type, tranz_id, *args):
        ''' Функция для кодирования тела пакета, т.е. кодирования транзакции.
        Принимает аргументы: Тип_транзакции_(int), Данные_транзакции_(int),
                          Сумма_в_копейка_(int)_(необязательно)

        >>> tranz_code(1, 2, 15)
        b'zz\\x01\\x00\\x00\\x00\\x02\\x00\\x00\\x00\\x00\\x00\\x00\\x00\\x0f'

        * Транзакция состоит из 2-х полей - тип транзакции и данные:
                * Тип транзакции:
                    * 0x00 - сервисная транзакция. Данные:
                        * 0x00 - включение
                        * 0x01 - перезагрузка
                        * 0x02 - выключение
                        * 0x03 - активация датчика X
                        * 0x04 - блокировка, требуется инкассация
                    * 0x01 - платёжная транзакция. Данные:
                        * 4 байта: id организации для перевода средств
                        * 8 байт: сумма транзакции в копейках
                    * 0x02 - инкассация. Данные:
                        * 4 байта: id сотрудника-инкассатора
                        * 8 байт: сумма инкассации в копейках
        '''
        def err_tranz():
            raise 'Неверный тип транзакции!'

        if tranz_type not in (0, 1, 2):
            err_tranz()

        if tranz_type == 0 and int(tranz_id) in (0, 1, 2, 3, 4):
            rez = bytes([tranz_type, tranz_id])
        elif (tranz_type == 1 or tranz_type == 2) and\
                isinstance(tranz_id, int) and len(args) == 1 and\
                isinstance(args[0], int):
            tranz_id = '{:0>32}'.format(bin(tranz_id)[2:])
            rez = bytes([tranz_type,
                         int(tranz_id[:8], 2),
                         int(tranz_id[8:16], 2),
                         int(tranz_id[16:24], 2),
                         int(tranz_id[24:], 2),
                         ])
            summ = '{:0>64}'.format(bin(args[0])[2:])
            rez += bytes([int(summ[:8], 2),
                          int(summ[8:16], 2),
                          int(summ[16:24], 2),
                          int(summ[24:32], 2),
                          int(summ[32:40], 2),
                          int(summ[40:48], 2),
                          int(summ[48:56], 2),
                          int(summ[56:], 2),
                          ])
        else:
            print(len(args))
            err_tranz()
        return rez

    def package_code(self):
        ''' Функция для всего тела пакет (заголовок + длина + дата-время +
        транзакция).
         Для работы функции, в объекте класса должны быть определены 3
        параметра:
            * self.date - объект datetime.datetime, при этом год должен быть
                            от 2000-го до 2099-го.
            * self.type - Тип транзакции (int)
            * self.data - Данные транзакции - список или кортеж с
                            данными (одно или два int-значения)
        '''
        date_byte = self.datetime_code(self.date)
        tranz_byte = self.tranz_code(self.type, *self.data)
        length_data_package = len(date_byte) + len(tranz_byte)
        # На длину пакета отвожу 1 байт, т.к. там максимум 18 байт тело.
        return b'zz' + bytes([length_data_package]) + date_byte + tranz_byte


def send_string(string):
    if not isinstance(string, bytes):
        string = bytes(string, 'utf-8')

    print('Отправляются данные: \'{}\''.format(string))
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((HOST, PORT))
    sock.sendall(string)
    recvd = str(sock.recv(1024), 'utf-8')
    sock.close()
    print('Получен ответ:', recvd)
    return recvd


def main():

    send_string('I_WANNA_PLAY')
    send_string('test')
    send_string('Test')

    tranz_01 = Tranzactions()
    tranz_01.date = datetime.datetime(year=2017, month=4, day=1, hour=5,
                                      minute=24, second=15)
    tranz_01.type = 1
    tranz_01.data = [17, 24]
    send_string(tranz_01.package_code())


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
