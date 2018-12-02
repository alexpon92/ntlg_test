"""
Дана статистика рекламных кампаний по дням.
Напишите алгоритм, который по паре дата-кампания ищет значение численного столбца.
Т. е. для даты '2018-01-01' и 'google' нужно получить число 25. Считайте, что все комбинации дата-кампания уникальны,
а список stats легко помещается в оперативной памяти.
"""

stats = [
    ['2018-01-01', 'google', 25],
    ['2018-01-01', 'yandex', 65],
    ['2018-01-01', 'market', 89],
    ['2018-01-02', 'google', 574],
    ['2018-01-02', 'yandex', 249],
    ['2018-01-02', 'market', 994],
    ['2018-01-03', 'google', 1843],
    ['2018-01-03', 'yandex', 1327],
    ['2018-01-03', 'market', 1764],
]


def hash_func(params):
    """
    :param params: params to make simple hash string from them
    :type params: list
    :return: some hash string for list of params
    :rtype: str
    """
    delimiter = '|'
    return delimiter.join(params)


def create_hash_map(some_list):
    """
    Getting first n-1 elements as unique identified and last as value for such key

    :param some_list: some list to be hashed
    :type some_list: list
    :return: hashed dict
    :rtype: dict
    """
    hashed_list = {}

    for row in some_list:
        hashed_list.setdefault(hash_func(params=row[:-1]), row[-1])

    return hashed_list


def search_by_map(params, hashed_list):
    """
    :param params: list of attributes by which search will be established
    :type params: list
    :param hashed_list: hashed list
    :type hashed_list: dict
    :return: value corresponds to params or none
    :rtype: int
    """
    key = hash_func(params)
    if key in hashed_list:
        return hashed_list[key]
    else:
        return None


hashed_stats = create_hash_map(stats)

print(search_by_map(params=['2018-01-01', 'google'], hashed_list=hashed_stats))
print(search_by_map(params=['2018-01-03', 'market'], hashed_list=hashed_stats))
