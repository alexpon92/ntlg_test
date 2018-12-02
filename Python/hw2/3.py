"""
Список поисковых запросов. Получить распределение количества слов в них.
Т. е. поисковых запросов из одного слова 5%, из двух - 7%, из трех - 3% итд.
"""
import re


def count_words(sentence):
    """
    :param sentence: some sentence
    :type sentence: str
    :return: number of words
    :rtype: int
    """
    return len(re.findall('(\d|\w)(\s)+(\d|\w)', sentence)) + 1


queries = [
    'смотреть сериалы онлайн',
    'новости спорта',
    'афиша кино',
    'курс доллара',
    'сериалы этим летом',
    'курс по питону',
    'сериалы про спорт',
]

distribution = {}
total_queries_count = 0

for query in queries:
    words_num = count_words(query)
    distribution.setdefault(words_num, 0)
    distribution[words_num] += 1
    total_queries_count += 1

for words_num, counter in distribution.items():
    # not using float(counter)/total_queries_count because using python 3
    distribution[words_num] = counter/total_queries_count * 100
    print(f'Number of words: {words_num}, distribution: {distribution[words_num]} %')
