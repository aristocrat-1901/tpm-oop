from enum import Enum
from encrypt_methods import enc_dec_replace, enc_dec_shift, enc_dec_replace_num
import sys


class Node:
    def __init__(self, data):
        self.data = data
        self.next = None


class Container:
    def __init__(self):
        self.start_node = None
        self.size = 0

    def add(self, data):
        if self.start_node is None:
            self.start_node = Node(data)
        else:
            n = self.start_node
            while n.next:
                n = n.next
            n.next = Node(data)

        self.size += 1

    def clear(self):
        self.start_node = None
        self.size = 0

    def read_from(self, stream):
        while line := stream.readline():
            text = Text()
            item = text.read_from(line)
            if item is not None:
                self.add(item)

    def write_to(self, stream):
        stream.write(f'Container has {self.size} elements\n\n')

        if self.start_node is not None:
            n = self.start_node
            while n:
                n.data.write_to(stream)
                n = n.next
            stream.write('\n')

    def sort(self):
        if self.start_node is None:
            print('Sorting not possible. Empty list')
        else:
            n1 = self.start_node
            n2 = self.start_node.next
            while n1 is not None:
                while n2 is not None:
                    if n1.data.number_of_symbols() < n2.data.number_of_symbols():  # > сортировка по убыванию длины строк
                        n1.data, n2.data = n2.data, n1.data
                    n2 = n2.next
                n1 = n1.next
                n2 = self.start_node

    def write_to_replace(self, stream):
        print("Only replacement method")

        if self.start_node is not None:
            n = self.start_node
            while n:
                n.data.write_to_replace(stream)
                n = n.next
            stream.write('\n')


class Text:
    def __init__(self):
        self.line_symbol = None  # строка символов
        self.key = None  # номер способа шифрования
        self.obj = None  # способ шифрования
        self.author = None  # владелец строки

    def read_from(self, line):
        list_param = line.rstrip('\n').split('; ')
        if len(list_param) < 3:
            print('Неверный формат входной строки!')
            return
        try:
            k = int(list_param[0])
        except ValueError:
            print('Первый параметр некорректен!')
            return
        self.line_symbol = list_param[1]
        self.author = list_param[2]
        if k == 1:
            self.key = Type.replacement
            self.obj = Replace()
            Replace.read_from(self.obj, self.line_symbol)
        elif k == 2:
            self.key = Type.shift
            self.obj = Shift()
            try:
                Shift.read_from(self.obj, list_param[3], self.line_symbol)
            except LookupError:
                print("Для 2 метода задан некорректный ключ!")
                return
        elif k == 3:
            self.key = Type.replacement_by_num
            self.obj = ReplaceNum()
            ReplaceNum.read_from(self.obj, self.line_symbol)
        else:
            print(f"Недопустимый тип метода {k}!")
            return

        return self

    def write_to(self, stream):
        if self.key == Type.replacement:
            try:
                stream.write('[Replacement method]\n')
                stream.write(f'String: {self.line_symbol}\n')
                stream.write(f'Author: {self.author}\n')
                stream.write(f'String length: {self.number_of_symbols()}\n')
                Replace.write_to(self.obj, stream)
            except OSError:
                print('Ошибка записи в файл!')
                sys.exit(1)
        elif self.key == Type.shift:
            try:
                stream.write('[Shift method]\n')
                stream.write(f'String: {self.line_symbol}\n')
                stream.write(f'Author: {self.author}\n')
                stream.write(f'String length: {self.number_of_symbols()}\n')
                Shift.write_to(self.obj, stream)
            except OSError:
                print('Ошибка записи в файл!')
                sys.exit(1)
        elif self.key == Type.replacement_by_num:
            try:
                stream.write('[Replacement by numbers method]\n')
                stream.write(f'String: {self.line_symbol}\n')
                stream.write(f'Author: {self.author}\n')
                stream.write(f'String length: {self.number_of_symbols()}\n')
                ReplaceNum.write_to(self.obj, stream)
            except OSError:
                print('Ошибка записи в файл!')
                sys.exit(1)
        else:
            stream.write('Ошибка при записи! Некорректный тип метода!\n')

    def write_to_replace(self, stream):
        if self.key == Type.replacement:
            try:
                stream.write('[Replacement method]\n')
                stream.write(f'String: {self.line_symbol}\n')
                stream.write(f'Author: {self.author}\n')
                stream.write(f'String length: {self.number_of_symbols()}\n')
                Replace.write_to(self.obj, stream)
            except OSError:
                print('Ошибка записи в файл!')
                sys.exit(1)

    def number_of_symbols(self):
        return len(self.line_symbol)


class Replace:
    def __init__(self):
        self.encrypt_line = None

    def read_from(self, line):
        self.encrypt_line = enc_dec_replace(line)

    def write_to(self, stream):
        stream.write(f'Encrypt message: {self.encrypt_line}\n')


class Shift:
    def __init__(self):
        self.key = None
        self.encrypt_line = None

    def read_from(self, key, line):
        try:
            self.key = int(key)
        except ValueError:
            print('Ключ для 2 метода должен быть числом!')
            return
        self.encrypt_line = enc_dec_shift(line, self.key)

    def write_to(self, stream):
        stream.write(f'Key = {self.key}\nEncrypt message : {self.encrypt_line}\n')


class ReplaceNum:
    def __init__(self):
        self.encrypt_line = None

    def read_from(self, line):
        self.encrypt_line = enc_dec_replace_num(line)

    def write_to(self, stream):
        stream.write(f'Encrypt message: {self.encrypt_line}\n')


class Type(Enum):
    replacement = 1
    shift = 2
    replacement_by_num = 3
