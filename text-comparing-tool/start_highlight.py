import sys
import highlight

if len(sys.argv) > 2:
    highlight.create_highligthted_file(sys.argv[1], sys.argv[2])
    print('Готово')
else:
    print('Введите имена двух файлов через пробел')