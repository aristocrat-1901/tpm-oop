import sys
from module import Container


def main():
    if len(sys.argv) != 3:
        print('\nФайлы ввода/вывода не выбраны! Будут использованы стандартные in.txt и out.txt\n')
        infile = 'in.txt'
        outfile = 'out.txt'
    else:
        infile = sys.argv[1]
        outfile = sys.argv[2]
    input_file = open(sys.argv[1], "r")

    print('Start')

    cont = Container()
    cont.read_from(input_file)

    print('Filled container')

    output_file = open(sys.argv[2], "w")
    cont.write_to(output_file)

    cont.clear()

    print('Empty container')
    cont.write_to(output_file)

    input_file.close()
    output_file.close()


if __name__ == '__main__':
    main()