import numpy as np
from numpy import linalg
import pandas as pd
import requests
from io import BytesIO
from zipfile import ZipFile

"""
Задание 1
Создайте numpy array с элементами от числа N до 0 
(например, для N = 10 это будет array([9, 8, 7, 6, 5, 4, 3, 2, 1, 0])).
"""


def create_numpy_arr1(n):
    """
    Create numpy arr with range
    """
    return np.array([i for i in range(n)][::-1])


def create_numpy_arr2(n):
    return np.arange(n - 1, -1, -1)


print('Task 1. Numpy arrays:')
print(create_numpy_arr1(10))
print(create_numpy_arr2(10))
print('=====================')

"""
Задание 2
Создайте диагональную матрицу с элементами от N до 0.
Посчитайте сумму ее значений на диагонали.
"""


def create_diag_matrix(n):
    return np.diag(np.arange(n - 1, -1, -1))


print('Task 2. Diag matrix:')
dm = create_diag_matrix(10)
print(dm)
print(f'Sum of diag elems: {sum(dm.diagonal())}')
print('=====================')

"""
Задание 3
Скачайте с сайта https://grouplens.org/datasets/movielens/ датасет любого размера.
Определите какому фильму было выставлено больше всего оценок 5.0.
"""


def get_zip_files():
    response = requests.get('http://files.grouplens.org/datasets/movielens/ml-latest-small.zip')
    return ZipFile(BytesIO(response.content))


def get_ratings_data_frame(zip_arch):
    """
    :return: pandas data frame with movies ratings
    """
    return pd.read_csv(zip_arch.open(name='ml-latest-small/ratings.csv'))


def get_movies_data_frame(zip_arch):
    """
    :return: pandas data frame with movies
    """
    return pd.read_csv(zip_arch.open(name='ml-latest-small/movies.csv'))


movies_zip = get_zip_files()
ratings = get_ratings_data_frame(movies_zip)
movies_info = get_movies_data_frame(movies_zip).set_index(keys='movieId', drop=False)

top_films = ratings.query('rating == {}'.format(5))

best_film_id = top_films['movieId'].value_counts().idxmax()

print(f'Task 3. Top movie: {movies_info.loc[best_film_id, "title"]}')
print('=====================')


"""
Задание 4
По данным файла power.csv посчитайте суммарное потребление стран Прибалтики (Латвия, Литва и Эстония)
категорий 4, 12 и 21 за период с 2005 по 2010 года. Не учитывайте в расчетах отрицательные значения quantity.
"""

power_data = pd.read_csv('power.csv')
sub_data = power_data.query('country in ("Latvia", "Lithuania", "Estonia") '
                            '& category in (4, 12, 21) & 2005 < year < 2010 & quantity >= 0')

print(f"Task 4. Total power consumption: {sub_data['quantity'].sum()}")
print('=====================')

"""
Задание 5
Решите систему уравнений:
4x + 2y + z = 4
x + 3y = 12
5y + 4z = -3
"""

left_side = np.array([
    [4, 2, 1],
    [1, 3, 0],
    [0, 5, 4]
])

right_side = np.array([4, 12, -3])
solution = linalg.solve(left_side, right_side)
x, y, z = solution

# check solution
if not np.allclose(np.dot(left_side, solution), right_side):
    raise RuntimeError('Incorrect solution!')

print(f'Task 5. Solution is: x = {x}, y = {y}, z = {z}')
print('=====================')
