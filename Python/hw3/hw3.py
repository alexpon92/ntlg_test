import requests

"""
1. Дан список вида:
data = [
    [13, 25, 23, 34],
    [45, 32, 44, 47],
    [12, 33, 23, 95],
    [13, 53, 34, 35],
]

Напишите функцию, которая возвращает сумму элементов на диагонали. Т. е. 13+32+23+35.
"""


def matrix_diagonal_sum(matrix):
    """
    :param matrix: matrix
    :type matrix: list
    :raise TypeError: wrong arg types
    :raise RuntimeError: Bad matrix dimension
    :return: main diagonal elements sum
    :rtype: int
    """
    if not isinstance(matrix, list):
        raise TypeError('Matrix should be passed as param')

    diag_sum = 0

    for index, row in enumerate(matrix):
        if not isinstance(row, list):
            raise TypeError('Matrix should be of type list')

        if len(row) < index:
            raise RuntimeError(f'Matrix rows is not correct. Cannot get diag elem. Row inx: {index}')

        if not isinstance(row[index], (int, float)):
            raise TypeError('Matrix should have only float and int elems')

        diag_sum += row[index]

    return diag_sum


data = [
    [13, 25, 23, 34],
    [45, 32, 44, 47],
    [12, 33, 23, 95],
    [13, 53, 34, 35],
]

print(f'Task 1. Diag sum: {matrix_diagonal_sum(data)}')
print('==============================================')


"""
Задание 2
Дан список чисел, часть из которых имеют строковый тип или содержат буквы. 
Напишите функцию, которая возвращает сумму квадратов элементов, которые могут быть числами.
data = [1, '5', 'abc', 20, '2']
"""


def sqr_sum(some_list):
    if not isinstance(some_list, (list, dict, tuple)):
        raise TypeError('Bad input param')

    sqrs_sum = 0
    for val in some_list:
        try:
            val = float(val)
        except ValueError:
            continue

        sqrs_sum += val * val

    return sqrs_sum


data = [1, '5', 'abc', 20, '2']
print(f'Task 2. Sqr sum: {sqr_sum(data)}')
print('==============================================')


"""
Задание 3
Напишите функцию, которая возвращает название валюты (поле 'Name') с максимальным значением курса 
с помощью сервиса https://www.cbr-xml-daily.ru/daily_json.js
"""


def get_currency_rate_and_name(currency):
    if 'Name' not in currency or 'Value' not in currency:
        raise RuntimeError('Malformed currency response info')
    return {'name': currency['Name'], 'rate': currency['Value']}


def get_currency_with_max_rate():
    """
    :return: currency with max rate
    :rtype: dict
    """
    response = requests.get('https://www.cbr-xml-daily.ru/daily_json.js')

    if response.status_code != 200:
        raise RuntimeError('Bad HTTP response code from currency server')

    json = response.json()

    max_currency = None

    if 'Valute' in json:
        for key, currency in json['Valute'].items():
            current_currency = get_currency_rate_and_name(currency)

            if max_currency is None or max_currency['rate'] < current_currency['rate']:
                max_currency = current_currency
    else:
        raise RuntimeError('Response format is incorrect, no Valute entry')

    return max_currency


print(f'Task 3. Currency with max rate: {get_currency_with_max_rate()["name"]}')
print('==============================================')

"""
Задание 4
Последнее упражнение с занятия
1. Добавьте в класс еще один формат, который возвращает название валюты (например, 'Евро').

2. Добавьте в класс параметр diff (со значениями True или False), который в случае значения 
True в методах eur и usd будет возвращать не курс валюты, а изменение по сравнению в прошлым значением.
"""


class Rate:
    def __init__(self, format='value', diff=False):
        self.format = format
        self.__diff = diff

    def exchange_rates(self):
        """
        Возвращает ответ сервиса с информацией о валютах в виде:

        {
            'AMD': {
                'CharCode': 'AMD',
                'ID': 'R01060',
                'Name': 'Армянских драмов',
                'Nominal': 100,
                'NumCode': '051',
                'Previous': 14.103,
                'Value': 14.0879
                },
            ...
        }
        """
        r = requests.get('https://www.cbr-xml-daily.ru/daily_json.js')
        return r.json()['Valute']

    def make_format(self, currency):
        """
        Возвращает информацию о валюте currency в двух вариантах:
        - полная информация о валюте при self.format = 'full':
        Rate('full').make_format('EUR')
        {
            'CharCode': 'EUR',
            'ID': 'R01239',
            'Name': 'Евро',
            'Nominal': 1,
            'NumCode': '978',
            'Previous': 79.6765,
            'Value': 79.4966
        }

        Rate('value').make_format('EUR')
        79.4966
        """
        response = self.exchange_rates()

        if currency in response:
            if self.format == 'full':
                return response[currency]

            if self.format == 'value':
                return response[currency]['Value']

            if self.format == 'name':
                return response[currency]['Name']

        return 'Error'

    def eur(self):
        """Возвращает курс евро на сегодня в формате self.format"""
        return self.__get_format_response('EUR')

    def usd(self):
        """Возвращает курс доллара на сегодня в формате self.format"""
        return self.__get_format_response('USD')

    def __get_currency_diff(self, currency_code):
        resp = self.exchange_rates()

        if currency_code in resp:
            return resp[currency_code]['Value'] - resp[currency_code]['Previous']

    def __get_format_response(self, currency_code):
        return self.make_format(currency_code) if not self.__diff else self.__get_currency_diff(currency_code)


print(f'Task 4. New "name" format: {Rate(format="name").eur()}')
print(f'Task 4. New "diff" format: {Rate(diff=True).eur()}')
print('==============================================')


"""
Задание 5
Напишите функцию, возвращающую сумму первых n чисел Фибоначчи
"""


from math import sqrt


def fib_elem(n):
    """
    Return nth elem of fib sequence, using golden section
    :param n: number of elem
    :rtype: float
    """
    return ((1 + sqrt(5)) ** n - (1 - sqrt(5)) ** n) / (2 ** n * sqrt(5))


def fib_sum(n):
    total = 0

    for elem_counter in range(n+1):
        total += fib_elem(elem_counter)

    return total


print(f'Task 5. First 5th elems fib sum: {fib_sum(5)}')
print('==============================================')


"""
Задание 6
Напишите функцию, преобразующую произвольный список вида ['2018-01-01', 'yandex', 'cpc', 100] 
в словарь {'2018-01-01': {'yandex': {'cpc': 100}}}
"""


def convert_to_dict(list):
    length = len(list)

    if length == 2:
        return {list[0]: list[1]}
    elif length > 2:
        return {list[0]: convert_to_dict(list[1::])}
    else:
        raise RuntimeError('Min length is 2')


print(f"Task 6. Convert to dict {convert_to_dict(['2018-01-01', 'yandex', 'cpc', 100])}")
print('==============================================')
