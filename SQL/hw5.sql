SELECT 'Пономарев Александр Андреевич';

-- Используя функцию определения размера таблицы, вывести top-5 самых больших таблиц базы.
SELECT information_schema.tables.table_name,
       pg_relation_size(information_schema.tables.table_name) as real_size,
       pg_size_pretty(pg_relation_size(information_schema.tables.table_name)) as pretty_size
FROM information_schema.tables
WHERE table_type = 'BASE TABLE'
  AND table_schema = 'public'
ORDER BY real_size DESC
LIMIT 5;

-- Используя функцию array_agg собрать в массив все фильмы, просмотренные пользователем. 
-- При этом повторов в списке контента быть не должно. Назовём эту конструкцию ЗАПРОС1. 
-- Выборка должна содержать два поля: userid и user_views
SELECT r.userid, array_agg(movieid) as user_views
FROM (SELECT userid, movieid FROM ratings GROUP BY userid, movieid) as r
GROUP BY r.userid;

-- Создайте таблицу user_movies_agg, в которую сохраните результат запроса
-- PS Добавил лимит для ограничения выборки и дальнейшей скорости
SELECT userid, user_views INTO public.user_movies_agg
FROM (SELECT r.userid, array_agg(movieid) as user_views
      FROM (SELECT userid, movieid FROM ratings GROUP BY userid, movieid LIMIT 50000) as r
      GROUP BY r.userid) aggregated_views;

-- Используя следующий синтаксис, создайте функцию cross_arr оторая принимает на вход два массива arr1 и arr2. 
-- Функция возвращает массив, который представляет собой пересечение контента из обоих списков.
-- PS: именованные аргументы нормально работают в 10ке для SQL диалекта
CREATE OR REPLACE FUNCTION cross_arr(arr1 int [], arr2 int [])
  RETURNS int []
language sql as
$FUNCTION$
SELECT ARRAY(SELECT UNNEST(arr1)
             INTERSECT
             SELECT UNNEST(arr2)
);
$FUNCTION$;

-- Сформируйте запрос следующего вида: достать из таблицы всевозможные наборы u1, r1, u2, r2.
-- u1 и u2 - это id пользователей r1 и r2 - соответствующие массивы рейтингов
-- Этот вариант - если для нас допустимы и различимы пары (u1, u2) и (u2, u1)
WITH user_pairs as (SELECT u1.userid as u1, u2.userid as u2, u1.user_views as uw1, u2.user_views as uw2
                    FROM (SELECT * FROM user_movies_agg) u1
                           CROSS JOIN (SELECT * FROM user_movies_agg) u2
                    WHERE u1.userid <> u2.userid)
SELECT u1, u2, cross_arr(uw1, uw2)
INTO common_user_views
FROM user_pairs;

-- Сформируйте запрос следующего вида: достать из таблицы всевозможные наборы u1, r1, u2, r2.
-- u1 и u2 - это id пользователей r1 и r2 - соответствующие массивы рейтингов
-- Этот вариант - если для нас недопустимы и неразличимы пары (u1, u2) и (u2, u1)
WITH user_pairs as (SELECT u1.userid as u1, u2.userid as u2, u1.user_views as uw1, u2.user_views as uw2
                    FROM (SELECT * FROM user_movies_agg) u1
                           INNER JOIN (SELECT * FROM user_movies_agg) u2 ON u1.userid < u2.userid
    )
SELECT u1, u2, cross_arr(uw1, uw2)
    INTO common_user_views
FROM user_pairs;
-- Далее продолжаем с вариантом с cross join и считаем зеркальные пары - разными


-- Отсортируйте выборку из common_user_views по длине crossed_array 
-- и оставите топ-10 пользователей с самыми большими пересечениями.
-- намеренно не убирал зеркальные пары!
SELECT u1, u2, array_length(cross_arr, 1) as cross_views_length
FROM common_user_views
ORDER BY cross_views_length DESC NULLS LAST
LIMIT 10;
                                     
-- Создайте по аналогии с cross_arr функцию diff_arr, которая вычитает один массив из другого.                                     
CREATE OR REPLACE FUNCTION diff_arr(arr1 int [], arr2 int [])
  RETURNS int [] language sql as
$FUNCTION$
SELECT ARRAY(SELECT UNNEST(arr1)
                 EXCEPT
                 SELECT UNNEST(arr2)
           );
$FUNCTION$;

-- Сформируйте рекомендации - для каждой пары посоветуйте для u1 контент, 
-- который видел u2, но не видел u1 (в виде массива).
SELECT common_user_views.u1 as u1,
       diff_arr(user_movies_agg.user_views, common_user_views.cross_arr) as recommendation,
       common_user_views.u2 as user_to_сcompare
FROM common_user_views
LEFT JOIN user_movies_agg ON common_user_views.u2 = user_movies_agg.userid;
                                    
                        
