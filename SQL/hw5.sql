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

