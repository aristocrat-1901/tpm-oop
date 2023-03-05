from enum import Enum
from encrypt_methods import enc_dec_replace, enc_dec_shift, enc_dec_replace_num


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
            item = text.read_from(stream, line)
            self.add(item)

    def write_to(self, stream):
        stream.write(f'Container has {self.size} elements\n\n')

        if self.start_node != None:
            n = self.start_node
            while n:
                Text.write_to(n.data, stream)
                n = n.next
            stream.write('\n')


class Text:
    def __init__(self):
        self.line_symbol = None  # строка символов
        self.key = None  # номер способа шифрования
        self.obj = None  # способ шифрования
        self.author = None  # владелец строки

    def read_from(self, stream, line):
        k = int(line)

        # text = Text()
        self.line_symbol = stream.readline().rstrip('\n')
        self.author = stream.readline().rstrip('\n')
        if k == 1:
            self.key = Type.replacement
            self.obj = Replace()
            Replace.read_from(self.obj, stream, self.line_symbol)
        elif k == 2:
            self.key = Type.shift
            self.obj = Shift()
            Shift.read_from(self.obj, stream, self.line_symbol)
        elif k == 3:
            self.key = Type.replacement_by_num
            self.obj = ReplaceNum()
            ReplaceNum.read_from(self.obj, stream, self.line_symbol)
        else:
            return 0

        return self

    def write_to(self, stream):
        if self.key == Type.replacement:
            stream.write('[Replacement method]\n')
            stream.write(f'String: {self.line_symbol}\n')
            stream.write(f'Author: {self.author}\n')
            stream.write(f'String length: {self.number_of_symbols()}\n')
            Replace.write_to(self.obj, stream)
        elif self.key == Type.shift:
            stream.write('[Shift method]\n')
            stream.write(f'String: {self.line_symbol}\n')
            stream.write(f'Author: {self.author}\n')
            stream.write(f'String length: {self.number_of_symbols()}\n')
            Shift.write_to(self.obj, stream)
        elif self.key == Type.replacement_by_num:
            stream.write('[Replacement by numbers method]\n')
            stream.write(f'String: {self.line_symbol}\n')
            stream.write(f'Author: {self.author}\n')
            stream.write(f'String length: {self.number_of_symbols()}\n')
            ReplaceNum.write_to(self.obj, stream)
        else:
            stream.write('Error type\n')

    def number_of_symbols(self):
        return len(self.line_symbol)


class Replace:
    def __init__(self):
        self.encrypt_line = None

    def read_from(self, stream, line):
        self.encrypt_line = enc_dec_replace(line)

    def write_to(self, stream):
        stream.write(f'Encrypt message: {self.encrypt_line}\n')


class Shift:
    def __init__(self):
        self.key = None
        self.encrypt_line = None

    def read_from(self, stream, line):
        self.key = int(stream.readline())
        self.encrypt_line = enc_dec_shift(line, self.key)

    def write_to(self, stream):
        stream.write(f'Key = {self.key}\nEncrypt message : {self.encrypt_line}\n')


class ReplaceNum:
    def __init__(self):
        self.encrypt_line = None

    def read_from(self, stream, line):
        self.encrypt_line = enc_dec_replace_num(line)

    def write_to(self, stream):
        stream.write(f'Encrypt message: {self.encrypt_line}\n')


class Type(Enum):
    replacement = 1
    shift = 2
    replacement_by_num = 3
