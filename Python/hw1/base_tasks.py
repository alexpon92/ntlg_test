import math

"""
1. Даны 2 строки long_phrase и short_phrase.
Напишите код, который проверяет действительно ли длинная фраза long_phrase длиннее короткой short_phrase.
И выводит True или False в зависимости от результата сравнения.
"""
long_phrase = 'Насколько проще было бы писать программы, если бы не заказчики'
short_phrase = '640Кб должно хватить для любых задач. Билл Гейтс (по легенде)'
print(f'Is long_phrase is longer than short_phrase: {len(long_phrase) > len(short_phrase)}')

"""
2. Дана строка text. Определите какая из двух букв встречается в нем чаще - 'а' или 'и'.
text = 'Если программист в 9-00 утра на работе, значит, он там и ночевал'
"""
text = 'Если программист в 9-00 утра на работе, значит, он там и ночевал'
total_len = len(text)
a_subs_count = total_len - len(text.replace('а', ''))
i_subs_count = total_len - len(text.replace('и', ''))

print(f'"а" occurrences: {a_subs_count}, "и" occurrences: {i_subs_count}')

"""
3. Дано значение объема файла в байтах. Напишите перевод этого значения в мегабайты в формате:
'Объем файла равен 213.68Mb'
"""
file_bytes_size = 55765123547
print(f'Объем файла равен {float(file_bytes_size) / 1024 / 1024 }Mb')

"""
4. Выведите на экран значение синуса 30 градусов с помощью метода math.sin.
"""
print(f'Sin val of 30 degrees is: {math.sin(math.radians(30))}')

"""
5. В прошлом задании у вас скорее всего не получилось точного значения 0.5 из-за конечной точности вычисления синуса. 
Но почему некоторые простые операции также могут давать неточный результат?
Попробуйте вывести на экран результат операции 0.1 + 0.2
"""
print(0.1 + 0.2)
# it's because of binary floating-point arithmetic
