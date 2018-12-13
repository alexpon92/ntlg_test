from datetime import datetime, timedelta
import calendar

"""
Задание 1
Напишите функцию date_range, которая возвращает список дней между датами start_date и end_date.
Даты должны вводиться в формате YYYY-MM-DD.
"""


def date_range(start_date, end_date):
    """
    :param start_date: start date
    :type start_date: str
    :param end_date: end date
    :type end_date: str
    :return: iterable object
    :rtype: list
    """
    start_date = datetime.strptime(start_date, '%Y-%m-%d')
    end_date = datetime.strptime(end_date, '%Y-%m-%d')

    for i in range((end_date - start_date).days):
        yield start_date + timedelta(days=i)


start = '2018-12-10'
end = '2018-12-20'

print(f'Task 1. List of dates: {list(date_range(start_date=start, end_date=end))}')
print('====================================')


"""
Задание 2
Дополните функцию из первого задания проверкой на корректность дат.
В случае неверного формата или если start_date > end_date должен возвращаться пустой список.
"""


def date_range_with_validation(start_date, end_date):
    try:
        start_date = datetime.strptime(start_date, '%Y-%m-%d')
        end_date = datetime.strptime(end_date, '%Y-%m-%d')
    except ValueError:
        return []

    for i in range((end_date - start_date).days):
        yield start_date + timedelta(days=i)


start = '2018-12-30'
end = '2018-12-20'

print(f'Task 2. List of dates with validation: {list(date_range_with_validation(start_date=start, end_date=end))}')
print('====================================')


"""
Дан поток дат в формате YYYY-MM-DD, в которых встречаются некорректные значения:
stream = ['2018-04-02', '2018-02-29', '2018-19-02']

Напишите функцию, которая проверяет эти даты на корректность.
Т. е. для каждой даты возвращает True (дата корректна) или False (некорректная дата). 
"""


def validate_date(date_str, format='%Y-%m-%d'):
    try:
        datetime.strptime(date_str, format)
    except ValueError:
        return False

    return True


print('Task 3. check valid dates')
stream = ['2018-04-02', '2018-02-29', '2018-19-02']
for date_str in stream:
    print(f'Is date {date_str} valid? Answer: {"Yes" if validate_date(date_str) else "No"}')
print('====================================')


"""
Задание 4
Напишите функцию, которая возвращает список дат с 1 по вчерашний день текущего месяца.
Если дан 1 день месяца, то возвращается список дней прошлого месяца.
"""


def prev_days():
    """
    :return: list of dates
    """
    date_to_work = datetime.today()

    if date_to_work.day == 1:
        start_date = (date_to_work - timedelta(days=1)).replace(day=1)
    else:
        start_date = date_to_work.replace(day=1)

    for i in range((date_to_work - start_date).days):
        yield (start_date + timedelta(days=i)).strftime('%Y-%m-%d')


print(f'Task 4. List of dates: {list(prev_days())}')
print('====================================')

"""
Задание 5
Напишите функцию, которая возвращает точную дату в формате YYYY-MM-DD по фразе:
1. 'today' - сегодняшнюю дату
2. 'last monday' -  прошлый понедельник
3. 'last day' - Последний день текущего месяца
"""


def date_macros(macros):
    today = datetime.today()
    if macros == 'today':
        return today.strftime('%Y-%m-%d')
    elif macros == 'last monday':
        return (today - timedelta(days=today.weekday())).strftime('%Y-%m-%d')
    elif macros == 'last day':
        m_range = calendar.monthrange(today.year, today.month)
        return today.replace(day=m_range[1]).strftime('%Y-%m-%d')
    else:
        raise ValueError('Macros may be: today, last monday, last day')


print(f'Task 5. Today: {date_macros("today")}. Last monday: {date_macros("last monday")}. \
Last day: {date_macros("last day")}.')
print('====================================')

"""
Задание 6
Напишите функцию, которая разбивает на недели с понедельника по воскресенье интервал дат между start_date и end_date.
Считайте, что входные данные всегда корректны. В ответ должны входить только полные недели.
"""


def get_full_weeks(start_date, end_date):
    """
    Return list of weeks. Each week is a list of dates formatted as YYYY-MM-DD

    :param start_date: Start date
    :type start_date: datetime
    :param end_date: Last date
    :type end_date: datetime
    :return: List with weeks
    :rtype: list
    """
    weeks = []

    closest_monday = (start_date + timedelta(days=-start_date.weekday(), weeks=1)).replace(
        hour=0, minute=0, second=0, microsecond=0
    )

    for weeks_num in range(int((end_date - closest_monday).days / 7)):
        weeks.append(
            [
                (closest_monday + timedelta(days=((weeks_num * 7) + i))).strftime('%Y-%m-%d') for i in range(7)
            ]
        )

    return weeks


print(f'Task 6. List of weeks: {get_full_weeks(datetime.today(), datetime(2019, 1, 1))}')
print('====================================')
