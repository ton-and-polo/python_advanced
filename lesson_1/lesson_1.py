import subprocess
import chardet
import sys

"""
1. Каждое из слов «разработка», «сокет», «декоратор» представить в строковом формате и проверить тип и содержание соответствующих переменных. Затем с помощью онлайн-конвертера преобразовать строковые представление в формат Unicode и также проверить тип и содержимое переменных.

2. Каждое из слов «class», «function», «method» записать в байтовом типе без преобразования в последовательность кодов (не используя методы encode и decode) и определить тип, содержимое и длину соответствующих переменных.

3. Определить, какие из слов «attribute», «класс», «функция», «type» невозможно записать в байтовом типе.

4. Преобразовать слова «разработка», «администрирование», «protocol», «standard» из строкового представления в байтовое и выполнить обратное преобразование (используя методы encode и decode).

5. Выполнить пинг веб-ресурсов yandex.ru, youtube.com и преобразовать результаты из байтовового в строковый тип на кириллице.

6. Создать текстовый файл test_file.txt, заполнить его тремя строками: «сетевое программирование», «сокет», «декоратор». Проверить кодировку файла по умолчанию. Принудительно открыть файл в формате Unicode и вывести его содержимое.
"""

# 1.
words_list = ['разработка', 'сокет', 'декоратор']

for word in words_list:
    print(word, type(word))

for word in words_list:
    b_word = word.encode(encoding='utf-8')
    print(b_word, type(b_word))

# 2.
words_list = [b'class', b'function', b'method']

for b_word in words_list:
    print(b_word, type(b_word), len(b_word))

# 3.
words_list = ['attribute', 'класс', 'функция', 'type']

for word in words_list:
    try:
        print(word.encode(encoding='ascii'))
    except UnicodeError:
        print(f'UnicodeError: {word}')

# 4.
words_list = ['разаботка', 'адмиинстрирование', 'protocol', 'standard']

for word in words_list:
    word = word.encode(encoding='utf-8')
    print(word)
    word = word.decode(encoding='utf-8')
    print(word)

# 5.


def run_ping(arguments: list):
    ping = subprocess.Popen(arguments, stdout=subprocess.PIPE)
    for pong in ping.stdout:
        print(pong, type(pong))
        print(pong.decode(encoding='utf-8'), type(pong.decode(encoding='utf-8')))


run_ping(['ping', '-c 5', 'yandex.com'])
run_ping(['ping', '-c 5', 'youtube.com'])

# 6.
words_list = ['сетевое програмирование', 'сокет', 'декоратор']
with open('test_file.txt', 'w', encoding='utf-8') as file:
    for word in words_list:
        file.write(f'{word}\n')

with open('test_file.txt', 'r') as file:
    result = chardet.detect(file.read().encode())
    print(result['encoding'])

# P.S.
print(sys.getdefaultencoding())