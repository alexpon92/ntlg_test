"""
Дан поток логов по количеству просмотренных страниц для каждого пользователя.
Список отсортирован по ID пользователя.
Вам необходимо написать алгоритм, который считает среднее значение просмотров на пользователя.
Т. е. надо посчитать отношение суммы всех просмотров к количеству уникальных пользователей.
Учтите, что весь список stream не помещается в оперативную память, т. е. его нужно обрабатывать поэлементно в цикле.
"""


def parse_stream_log(stream_log_line):
    """
    :param stream_log_line: some stream line
    :type stream_log_line: str
    :return: divided by delimiter list of values
    :rtype: list
    """
    return stream_log_line.split(',')


stream = [
    '2018-01-01,user1,3',
    '2018-01-07,user1,4',
    '2018-03-29,user1,1',
    '2018-04-04,user1,13',
    '2018-01-05,user2,7',
    '2018-06-14,user3,4',
    '2018-07-02,user3,10',
    '2018-03-21,user4,19',
    '2018-03-22,user4,4',
    '2018-04-22,user4,8',
    '2018-05-03,user4,9',
    '2018-05-11,user4,11',
]

unique_users_count = 0
curr_user = None
total_watch = 0

for watch_log in stream:
    stream_entity = parse_stream_log(stream_log_line=watch_log)
    if len(stream_entity) != 3:
        # skip bad logs entities
        continue

    if curr_user is None or curr_user != stream_entity[1]:
        curr_user = stream_entity[1]
        unique_users_count += 1

    watch_count = int(stream_entity[2])
    total_watch += watch_count


print(total_watch / unique_users_count)
