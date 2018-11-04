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
SELECT userid, user_views INTO public.user_movies_agg
FROM (SELECT r.userid, array_agg(movieid) as user_views
      FROM (SELECT userid, movieid FROM ratings GROUP BY userid, movieid) as r
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


