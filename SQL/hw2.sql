SELECT 'ФИО: Пономарев Александр Андреевич';

-- 1.1: SELECT , LIMIT - выбрать 10 записей из таблицы rating (Для всех дальнейших запросов выбирать по 10 записей, 
-- если не указано иное)

SELECT *
FROM ratings
LIMIT 10;

------------------------------------

-- 1.2: WHERE, LIKE - выбрать из таблицы links всё записи,
-- у которых imdbid оканчивается на "42", а поле movieid между 100 и 1000';

SELECT *
FROM links l
WHERE l.imdbid LIKE '%42'
  AND l.movieid BETWEEN 100 AND 1000;

------------------------------------

-- 2.1 INNER JOIN выбрать из таблицы links все imdbId, которым ставили рейтинг 5

SELECT DISTINCT l.imdbid
FROM links l
       INNER JOIN ratings r ON l.movieid = r.movieid
WHERE r.rating = 5
LIMIT 10;

------------------------------------

-- 3.1 COUNT() Посчитать число фильмов без оценок

SELECT count(DISTINCT l.movieid)
FROM links l
  LEFT JOIN ratings r ON l.movieid = r.movieid
WHERE r.movieid IS NULL
LIMIT 10;

------------------------------------

-- 3.2 GROUP BY, HAVING вывести top-10 пользователей, у который средний рейтинг выше 3.5

SELECT r.userid, avg(r.rating) as average_ratio
FROM ratings r

GROUP BY r.userid
HAVING avg(r.rating) > 3.5

ORDER BY avg(r.rating) DESC
LIMIT 10;

------------------------------------

-- 4.1 Подзапросы: достать любые 10 imbdId из links у которых средний рейтинг больше 3.5.

-- correlated sub-queries
-- DANGER!!! DRASTICALLY BAD PERFORMANCE!! ONLY THEORY EXAMPLE!!!
SELECT l.imdbid
FROM links l
WHERE EXISTS(
  SELECT 1
  FROM ratings r
  WHERE r.movieid = l.movieid
  GROUP BY r.movieid
  HAVING avg(r.rating) > 3.5
)
ORDER BY l.imdbid ASC
LIMIT 10;

-- non-correlated sub-queries
-- a bit harder for query plan, but faster exec time (because of hash join)
SELECT l.imdbid
FROM links l
WHERE l.movieid IN (
  SELECT r.movieid
  FROM ratings r
  GROUP BY r.movieid
  HAVING avg(r.rating) > 3.5
)
ORDER BY l.imdbid ASC
LIMIT 10;

-- inner join
-- easier for query plan, but much slower exec time
SELECT l.imdbid, avg(r.rating) as average_ratio
FROM links l
  INNER JOIN ratings r ON r.movieid = l.movieid

GROUP BY l.imdbid
HAVING avg(r.rating) > 3.5

ORDER BY l.imdbid ASC
LIMIT 10;

------------------------------------

-- 4.2 Common Table Expressions: посчитать средний рейтинг по пользователям, у которых более 10 оценок.
-- Нужно подсчитать средний рейтинг по все пользователям,
-- которые попали под условие - то есть в ответе должно быть одно число.

-- sub-query
WITH users_with_10_or_more_ratings as (
    SELECT r.userid
    FROM ratings r
    GROUP BY r.userid
    HAVING count(r.rating) > 10
    )
SELECT avg(r2.rating)
FROM ratings r2
WHERE r2.userid IN (SELECT userid FROM users_with_10_or_more_ratings);

-- join
WITH users_with_10_or_more_ratings as (
    SELECT r.userid
    FROM ratings r
    GROUP BY r.userid
    HAVING count(r.rating) > 10
    )
SELECT avg(r2.rating)
FROM ratings r2
       inner join users_with_10_or_more_ratings as u10 ON u10.userid = r2.userid;


------------------------------------
