"""
Дан список с визитами по городам и странам. Напишите код, который возвращает отфильтрованный список geo_logs,
содержащий только визиты из России. Считайте, что список geo_logs легко помещается в оперативной памяти.
"""


def filter_russ_visits(visit):
    """
    :param visit: visit info
    :type visit: dict
    :return: 1 - if its Russiona visit, 0 otherwise
    :rtype: int
    """
    for key, value in visit.items():
        if "Россия" in value:
            return 1
    return 0


geo_logs = [
    {"visit1": ["Москва", "Россия"]},
    {"visit2": ["Дели", "Индия"]},
    {"visit3": ["Владимир", "Россия"]},
    {"visit4": ["Лиссабон", "Португалия"]},
    {"visit5": ["Париж", "Франция"]},
    {"visit6": ["Лиссабон", "Португалия"]},
    {"visit7": ["Тула", "Россия"]},
    {"visit8": ["Тула", "Россия"]},
    {"visit9": ["Курск", "Россия"]},
    {"visit10": ["Архангельск", "Россия"]},
]

print(list(filter(filter_russ_visits, geo_logs)))
