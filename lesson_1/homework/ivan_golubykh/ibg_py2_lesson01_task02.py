#!/usr/bin/python3
import unittest
import pytest
import hashlib
__author__ = 'Иван Голубых'


def calc_hash(string, method):
    ''' Функция должна получать строку и метод вычисления хэш-суммы, а на
    выходе выдавать хеш-сумму строки.
     Допустимые методы: 'whirlpool', 'sha384', 'MD4', 'SHA1',
    'ecdsa-with-SHA1', 'SHA224', 'DSA-SHA', 'sha256', 'SHA256', 'SHA512',
    'sha1', 'sha512', 'md4', 'RIPEMD160', 'dsaEncryption', 'MD5', 'DSA',
    'sha', 'dsaWithSHA', 'md5', 'ripemd160', 'SHA', 'SHA384', 'sha224'.
    '''
    pass


def main():
    ''' Главная функция должна:
    1) открыть файл, построчное считать данные и обработать их функцией
     calc_hash. Результат сохранить в кортеж.
    2) Записать кортеж в файл начиная с его начала.
    3) обрезать лишнюю длину файла
    4) вернуть значение 0 (ноль) при успехе
    '''
    pass
    print(hashlib.algorithms_available)
    func = getattr(hashlib, "md5")
    print('строка:', hashlib.md5(b'I love Python').hexdigest(),
          ' \nпоследовательность байтов:',
          str(func(b'I love Python').digest()))
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
