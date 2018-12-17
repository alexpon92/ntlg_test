import pandas as pd
from datetime import timedelta

"""
Задание 1
Используем файл keywords.csv.
Необходимо написать гео-классификатор, который каждой строке сможет выставить географическую принадлежность
определенному региону. Т.е. если поисковый запрос содержит название города региона,
то в столбце 'region' пишется название этого региона.
Если поисковый запрос не содержит названия города, то ставим 'undefined'.
Правила распределения по регионам Центр, Северо-Запад и Дальний Восток:
geo_data = {
    'Центр': ['москва', 'тула', 'ярославль'],
    'Северо-Запад': ['петербург', 'псков', 'мурманск'],
    'Дальний Восток': ['владивосток', 'сахалин', 'хабаровск']
}
Результат классификации запишите в отдельный столбец region.
"""

geo_data = {
    'Центр': ['москва', 'тула', 'ярославль'],
    'Северо-Запад': ['петербург', 'псков', 'мурманск'],
    'Дальний Восток': ['владивосток', 'сахалин', 'хабаровск']
}


def set_geo_zone(row, geo_dict):
    for key, values in geo_dict.items():
        if any(value in row['keyword'].lower() for value in values):
            return key

    return 'undefined'


keywords = pd.read_csv('keywords.csv')

keywords['region'] = keywords.apply(set_geo_zone, axis=1, geo_dict=geo_data)

print('Task 1. Adding geo zones:')
print(keywords['region'].value_counts())
print('==========================')

"""
Задание 2
Напишите функцию, которая классифицирует фильмы из материалов занятия по следующим правилам:
    - оценка 2 и меньше - низкий рейтинг
    - оценка 4 и меньше - средний рейтинг
    - оценка 4.5 и 5 - высокий рейтинг

Результат классификации запишите в столбец class
"""

ratings = pd.read_csv('ml-latest-small/ratings.csv')
movies = pd.read_csv('ml-latest-small/movies.csv')

avg_ratio = ratings[['movieId', 'rating']].groupby('movieId').agg({'rating': ['mean']})


def get_film_class(row, avg_rat):
    if row['movieId'] in avg_rat.index:
        rating = avg_rat.loc[row['movieId'], {'rating': 'mean'}][0]
        if rating <= 2:
            return 'низкий рейтинг'
        elif 2 < rating <= 4:
            return 'средний рейтинг'
        else:
            return 'высокий рейтинг'

    return 'undefined'


movies['class'] = movies.apply(get_film_class, axis=1, avg_rat=avg_ratio)

print('Task 2. Adding class to movies')
print(movies.head())
print('==========================')

""" 
Задание 3
Посчитайте среднее значение Lifetime киноманов (пользователи, которые поставили 100 и более рейтингов).
Под Lifetime понимается разница между максимальным и минимальным значением timestamp для каждого пользователя.
Ответ дайте в днях
"""

ratings = pd.read_csv('ml-latest-small/ratings.csv')

users = ratings.groupby('userId').agg({'timestamp': ['min', 'max'], 'movieId': 'count'})
users = users[users['movieId']['count'] >= 100]
users['Lifetime'] = users.apply(lambda row: row['timestamp']['max'] - row['timestamp']['min'], axis=1)

avg_life_time = round(users['Lifetime'].mean())

print(f'Task 3. Average Lifetime of film lover is {timedelta(seconds=avg_life_time).days} days')
print('==========================')


"""
Задание 4
Есть мнение, что "раньше снимали настоящее кино, не то что сейчас". 
Ваша задача проверить это утверждение, используя файлы с рейтингами фильмов из материалов занятия.
Т.е. проверить верно ли, что с ростом года выпуска фильма его средний рейтинг становится ниже.

При этом мы не будем затрагивать субьективные факторы выставления этих рейтингов, а пройдемся по следующему алгоритму:
1. В переменную years запишите список из всех годов с 1950 по 2010.
2. Напишите функцию production_year, которая каждой строке из названия фильма выставляет год выпуска. 
    Не все названия фильмов содержат год выпуска в одинаковом формате, поэтому используйте следующий алгоритм:
    - для каждой строки пройдите по всем годам списка years
    - если номер года присутствует в названии фильма, то функция возвращает этот год как год выпуска
    - если ни один из номеров года списка years не встретился в названии фильма, то возвращается 1900 год
3. Запишите год выпуска фильма по алгоритму пункта 2 в новый столбец 'year'

4. Посчитайте средний рейтинг всех фильмов для каждого значения столбца 'year' 
    и отсортируйте результат по убыванию рейтинга
"""

movies = pd.read_csv('ml-latest-small/movies.csv')
ratings = pd.read_csv('ml-latest-small/ratings.csv')

years = [str(i) for i in range(1950, 2011)]


def get_production_year(row, years_list):
    for year in years_list:
        if year in row['title']:
            return year

    return 1900


movies['year'] = movies.apply(get_production_year, axis=1, years_list=years)

ratings = ratings.join(other=movies, on='movieId', how='left', rsuffix='_movies')
ratings = ratings[['year', 'rating']].groupby('year').mean().sort_values('rating', ascending=False)

print('Task 4. Top rated movies production years:')
print(ratings.head(5))
print('==========================')
