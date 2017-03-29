#!/usr/bin/python3
import unittest
import pytest
import hashlib
__author__ = 'Иван Голубых'


def calc_hash(string, method):
    ''' Функция должна получать строку и метод вычисления хэш-суммы, а на
    выходе выдавать хеш-сумму строки.
     Допустимые методы: sha224, sha1, md5, sha384, sha256, sha512.
    '''
    if method in hashlib.algorithms_guaranteed:
        if isinstance(string, str):
            string = string.encode()
        if isinstance(string, bytes):
            func = getattr(hashlib, method)
            return func(string).hexdigest()
        print('Ошибка: Недопустимые данные. Должна быть строка или байты')
        return False
    print('Ошибка: Недопустимый метод. Допустимые методы такие: ' +
          ', '.join(hashlib.algorithms_guaranteed))
    return False


def main():
    ''' Главная функция должна:
    1) открыть файл, построчное считать данные и обработать их функцией
     calc_hash. Результат сохранить в кортеж.
    2) Записать кортеж в файл начиная с его начала.
    3) обрезать лишнюю длину файла
    4) вернуть значение 0 (ноль) при успехе
    '''
    file = open('../need_hashes.csv', 'rb+')
    rezault = ''
    for x in file:
        data_string = x.decode().split(';')
        if len(data_string) > 2:
            rezault += calc_hash(data_string[0], data_string[1]) + '\n'
    file.seek(0, 0)
    file.write(rezault.encode())
    file.truncate()
    file.close()
    return 0


class TestThis(unittest.TestCase):
    def test_calc_hash_md5(self):
        self.assertEqual(calc_hash('I love Python', 'md5'),
                         '27eb2f69c24aa5f3503a6ae610f23a83')

    def test_calc_hash_sha1(self):
        self.assertEqual(calc_hash('I love Python', 'sha1'),
                         '9233eac58259dd3a13d6c9c59f8001823b6b1fee')

    def test_calc_hash_sha512(self):
        self.assertEqual(calc_hash('I love Python', 'sha512'),
                         '24e8aa2f457ee5108f1b308a645db3c59494f39d85a3fd9f9662'
                         '02925e793fe254006851975d18c0c4b0b70c54c05e2c8cb6272b'
                         '9dd771fed2d0b34cf852df56')

    def test_main(self):
        self.assertEqual(main(), 0)


if __name__ == '__main__':
    main()
