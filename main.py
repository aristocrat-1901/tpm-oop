import sys
from module import Container


def main():
    if len(sys.argv) != 3:
        print('\nФайлы ввода/вывода не выбраны!')
        infile = 'in.txt'
        outfile = 'out.txt'
        print(f'Будут использованы стандартные {infile} и {outfile}!\n')
    else:
        infile = sys.argv[1]
        outfile = sys.argv[2]

    input_file = open(infile, "r")
    print('Start')
    cont = Container()
    cont.read_from(input_file)
    input_file.close()

    print('Filled container')
    cont.sort()  # сортировка контейнера по количеству символов в строке
    output_file = open(outfile, "w")
    cont.write_to(output_file)
    # cont.write_to_replace(output_file) # запись в файл только одного метода Replace

    cont.clear()
    print('Empty container')
    cont.write_to(output_file)
    output_file.close()


if __name__ == '__main__':
    main()
