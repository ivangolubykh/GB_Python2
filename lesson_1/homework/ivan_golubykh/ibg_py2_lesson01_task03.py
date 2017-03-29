#!/usr/bin/python3
import unittest
import hashlib
import os
import glob
from zipfile import ZipFile
import magic  # pip3 install python-magic
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
    path, file = os.path.split(file_name_md5)
    if file in os.listdir(dir_name):
        return "Ошибка: файл " + file_name_md5 + ' уже есть в той же папке, '\
            'что и обрабатываемые файлы. Вносит изменения опасно.'
    md5_file = open(file_name_md5, 'w')
    count = 0
    list_dir = os.listdir(dir_name)
    list_dir.sort()
    for x in list_dir:
        file = open(os.path.join(dir_name, x), 'rb')
        data = file.read()
        file.close()
        md5_file.write(hashlib.md5(data).hexdigest()+'\n')
        count += 1
    md5_file.close()
    return count


def join_file(dir_name, file_name_md5, file_name_joined):
    ''' Функция "склеивания" файла на основе упорядоченных хэш-сумм.
     Принимает имя директории с файлами-кусочками, имя файла с
    хэш-суммами, имя выходного файла.
     Возвращает размер полученного файла.
    '''
    ''' Был выбор либо 2 раза читать все файлы (для расчёта сумм и для
    склеивания), либо все файлы загрузить в память. Я решил, что рациональней
    читать файлы 2 раза, хот это и медленнее, зато можно обрабатывать очень
    большие файл в любом количестве, лишь бы любой отдельный файл уместился
    в оперативной памяти.
    '''
    path, file = os.path.split(file_name_md5)
    block_files = [file]  # список файлов, которые не надо обрабатывать
    path, file = os.path.split(file_name_joined)
    block_files.append(file)
    hash_file = {}  # словарь соотнесения хешей с именами файлов
    for x in os.listdir(dir_name):
        if x not in block_files:
            file = open(os.path.join(dir_name, x), 'rb')
            data_file = file.read()
            hash_file[hashlib.md5(data_file).hexdigest()] = x
            file.close()

    file_joined = open(file_name_joined, 'wb')
    file_md5 = open(file_name_md5, 'r')
    for x in file_md5:
        file = open(os.path.join(dir_name, hash_file[x.rstrip()]), 'rb')
        file_joined.write(file.read())
        file.close()
    file_md5.close()
    file_joined.close()
    return os.path.getsize(file_name_joined)


def main():
    ''' Главная функция должна:
    1) распаковать все архивы в нужном каталоге
    2) Вызвать функцию склеивания для каждого каталога и получить склеенные
    файлы.
    3) определить тип получившихся фалов и вывести в консоль.
    4) вернуть значение 0 (ноль), когда будет написана отлажена эта функция.
    '''
    # 1) распаковать все архивы в нужном каталоге:
    start_dir = os.getcwd()
    os.chdir('../files')
    for zip_filename in glob.iglob('*.zip'):
        zip_handler = ZipFile(zip_filename, 'r')
        zip_handler.extractall()

    # 2) Вызвать функцию склеивания для каждого каталога и получить склеенные
    # файлы.
    dir_list = tuple(x for x in os.listdir() if os.path.isdir(x))
    for x in dir_list:
        join_file(x, os.path.join(x, 'parts.md5'), x+'.joined')

        # 3) определить тип получившихся фалов и вывести в консоль.
        print('"'+x+'.joined" - ', magic.from_file(x+'.joined'))

    os.chdir(start_dir)
    return 0


class TestThis(unittest.TestCase):
    def test_split_file(self):
        ''' Для этого теста создал папку test_split_file с 1 фалом
        '''
        self.assertEqual(split_file('./test_split_file/README.MD', 1000),
                         4)

    def test_creade_mda_file(self):
        ''' Для этого теста создал папку test_creade_mda_file с 4 фалами
        '''
        self.assertEqual(creade_mda_file('./test_creade_mda_file',
                                         './test_creade_mda_file.md5'
                                         ),
                         4)

    def test_join_file(self):
        ''' Для этого теста использую папку test_creade_mda_file. Использую
        только имена файлов без расширения.
        '''
        self.assertEqual(join_file('./test_creade_mda_file',
                                   './test_creade_mda_file.md5',
                                   'README.MD_joined'), 3093)

    def test_main(self):
        self.assertEqual(main(), 0)


if __name__ == '__main__':
    main()
