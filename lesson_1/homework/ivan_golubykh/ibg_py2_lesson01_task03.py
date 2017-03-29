#!/usr/bin/python3
import unittest
import hashlib
import os
__author__ = 'Иван Голубых'


def split_file(filename, length_fragment):
    ''' Функция разбиения файла на кусочки указанной длины.
     Принимает имя исходного файла и размер кусков в байтах.
     Возвращает количество получившихся файлов-фрагментов.
    '''
    if os.path.isfile(filename):
        file = open(filename, 'rb')
        if os.path.getsize(filename) < length_fragment:
            length_fragment = os.path.getsize(filename)
        count = 0
        for _ in range(0, os.path.getsize(filename),
                       length_fragment):
            count += 1
            data = file.read(length_fragment)
            file_i = open(filename+'_'+str(count), 'wb')
            file_i.write(data)
            file_i.close()
        fragment = file.read(5093)
        file.close()
        return count
    print('Ошибка: файл не существует.')
    return None


def creade_mda_file(dir_name, file_name_md5):
    ''' Функция составления текстового файла с md5-хэшами файлов в
    указанной директории.
     Принимает имя директории с файлами, имя файла для записи результатов.
     Возвращает количество просмотренных файлов.
    '''
    pass


def join_file(dir_name, file_name_md5, file_name_joined):
    ''' Функция "склеивания" файла на основе упорядоченных хэш-сумм.
    Используются только имена файлов без расширения.
     Принимает имя директории с файлами-кусочками, имя файла с
    хэш-суммами, имя выходного файла.
     Возвращает размер полученного файла.
    '''
    pass


def main():
    ''' Главная функция должна:
    1) распаковать все архивы в нужном каталоге
    2) Вызвать функцию склеивания для каждого каталога и получит склеенные
    файлы.
    3) определить тип получившихся фалов и вывести в консоль.
    4) вернуть значение 0 (ноль), когда будет написана отлажена эта функция.
    '''
    return 1


class TestThis(unittest.TestCase):
    def test_split_file(self):
        ''' Для этого теста создал папку test_split_file с 1 фалом
        '''
        self.assertEqual(split_file('./test_split_file/README.MD', 1000),
                         4)

    def test_creade_mda_file(self):
        ''' Для этого теста создал папку test_creade_mda_file с 3 фалами
        '''
        self.assertEqual(creade_mda_file('./test_creade_mda_file',
                                         './test_creade_mda_file/parts.md5'
                                         ),
                         3)

    def test_join_file(self):
        ''' Для этого теста использую папку test_creade_mda_file. Использую
        только имена файлов без расширения.
        '''
        self.assertEqual(join_file('./test_split_file/README.MD', 1000),
                         2313)

    def test_main(self):
        self.assertEqual(main(), 0)


if __name__ == '__main__':
    main()
