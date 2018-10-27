-- Вывести список пользователей в формате userId, movieId, normed_rating, avg_rating где
-- userId, movieId - без изменения
-- для каждого пользователя преобразовать рейтинг r в нормированный
-- normed_rating=(r - r_min)/(r_max - r_min), 
-- где r_min и r_max соответственно минимально и максимальное значение рейтинга у данного пользователя
-- avg_rating - среднее значение рейтинга у данного пользователя
-- Вывести первые 30 таких записей

SELECT
       userId,
       movieId,
       rating,
       (rating - MIN(rating) OVER uw) / (MAX(rating) OVER uw - MIN(rating) OVER uw)
         as normed_rating,
       avg(rating) OVER (PARTITION BY userid) as avergare_rating
FROM ratings r
WINDOW uw as (PARTITION BY userid)
LIMIT 30;
