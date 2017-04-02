#!/usr/bin/python3
# Клиент игры "Запоминалка"

import socket

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
    # __add__  ->  +


if __name__ == '__main__':
    main()
