-- Creating data structure --

--- SQL 1 (Queries group) ---

-- registered - just registered user
-- on_verification - on security verification (licence check)
-- verified - verified docs, approved users
-- declined - bad licence
-- banned - banned users for rules violation
-- additional_docs_required - additional docs is required for security check
CREATE TYPE user_status_enum AS ENUM ('registered', 'on_verification', 'verified', 'declined', 'banned', 'additional_docs_required');

CREATE TABLE users (
  id     bigserial,
  phone  varchar(15),
  name   varchar(255),
  email  varchar(255),
  status user_status_enum NOT NULL,
  PRIMARY KEY (id)
);

-- create table for partitioning
create table if not exists users_odd
(
  CHECK (id % 2 = 1)
)
  INHERITS (users);

create table if not exists users_even
(
  CHECK (id % 2 = 0)
)
  INHERITS (users);

-- create partitioning rules
CREATE OR REPLACE RULE insert_users_with_even_id AS ON INSERT
  TO users WHERE id % 2 = 0 DO INSTEAD INSERT INTO users_even
                                       VALUES (NEW.*);

CREATE OR REPLACE RULE insert_users_with_odd_id AS ON INSERT
  TO users WHERE id % 2 = 1 DO INSTEAD INSERT INTO users_odd
                                       VALUES (NEW.*);

-- available_for_rent - free car
-- in_rent - car, which in the rent at the moment
-- in_service - in service (broken, etc.)
-- decommissioned - totally destroyed car
CREATE TYPE car_status_enum AS ENUM ('available_for_rent', 'in_rent', 'in_service', 'decommissioned');

CREATE TABLE cars (
  id     serial,
  number varchar(9)      NOT NULL,
  model  varchar(50),
  status car_status_enum NOT NULL,
  PRIMARY KEY (id),
  UNIQUE (number)
);

CREATE TABLE tariff (
  id               SERIAL,
  price_per_minute decimal(6, 2) NOT NULL CHECK (price_per_minute >= 0),
  PRIMARY KEY (id)
);

CREATE TABLE car2tariff (
  car_id    integer NOT NULL REFERENCES cars (id),
  tariff_id integer NOT NULL REFERENCES tariff (id),
  PRIMARY KEY (car_id, tariff_id)
);

CREATE TABLE rents (
  id          bigserial,
  user_id     bigint references users (id),
  cost        decimal(10, 2) DEFAULT 0 CHECK (cost >= 0),
  car_id      integer                  NOT NULL REFERENCES cars (id),
  tariff_id   integer                  NOT NULL REFERENCES tariff (id),
  started_at  TIMESTAMP WITH TIME ZONE NOT NULL,
  finished_at TIMESTAMP WITH TIME ZONE,
  PRIMARY KEY (id)
);
-- Add indexes on foreign keys
CREATE INDEX rent_user_id_idx
  ON rents (user_id);
CREATE INDEX rent_car_id_idx
  ON rents (car_id);
CREATE INDEX rent_tariff_id_idx
  ON rents (tariff_id);

-- create partitioning tables
create table if not exists rents_odd
(
  CHECK (id % 2 = 1)
)
  INHERITS (rents);

create table if not exists rents_even
(
  CHECK (id % 2 = 0)
)
  INHERITS (rents);

-- create partitioning rules
CREATE OR REPLACE RULE insert_rents_with_even_id AS ON INSERT
  TO rents WHERE id % 2 = 0 DO INSTEAD INSERT INTO rents_even
                                       VALUES (NEW.*);

CREATE OR REPLACE RULE insert_rent_with_odd_id AS ON INSERT
  TO rents WHERE id % 2 = 1 DO INSTEAD INSERT INTO rents_odd
                                       VALUES (NEW.*);

-----------------------------------------------------------------------------------------------------------------
-- SQL 2 (Queries group)
-- Filling data in users
INSERT INTO users (id, phone, name, email, status)
VALUES (nextval('users_id_seq'), '71111111111', 'Some name', 'example@bk.ru', 'registered'),
       (nextval('users_id_seq'), '71111111112', 'Some name2', 'example2@bk.ru', 'on_verification'),
       (nextval('users_id_seq'), '71111111113', 'Some name3', 'example3@bk.ru', 'verified'),
       (nextval('users_id_seq'), '71111111114', 'Some name4', 'example4@bk.ru', 'verified'),
       (nextval('users_id_seq'), '71111111115', 'Some name5', 'example5@bk.ru', 'verified'),
       (nextval('users_id_seq'), '71111111116', 'Some name6', 'example6@bk.ru', 'verified'),
       (nextval('users_id_seq'), '71111111117', 'Some name7', 'example7@bk.ru', 'verified'),
       (nextval('users_id_seq'), '71111111118', 'Some name8', 'example8@bk.ru', 'verified'),
       (nextval('users_id_seq'), '71111111119', 'Some name9', 'example9@bk.ru', 'additional_docs_required'),
       (nextval('users_id_seq'), '71111111121', 'Some name10', 'example10@bk.ru', 'banned'),
       (nextval('users_id_seq'), '71111111122', 'Some name11', 'example11@bk.ru', 'declined');

-- Put some data in cars table
INSERT INTO cars (id, number, model, status)
VALUES (nextval('cars_id_seq'), 'а123фф777', 'Bugatti', 'available_for_rent'),
       (nextval('cars_id_seq'), 'а124фф777', 'Lambo', 'in_rent'),
       (nextval('cars_id_seq'), 'а125фф777', 'Lada', 'in_rent'),
       (nextval('cars_id_seq'), 'а126фф777', 'Camry', 'in_service'),
       (nextval('cars_id_seq'), 'а127фф777', 'Bugatti', 'decommissioned');

-- Put some data in tariff table
INSERT INTO tariff (id, price_per_minute)
VALUES (nextval('tariff_id_seq'), 50),
       (nextval('tariff_id_seq'), 5),
       (nextval('tariff_id_seq'), 10);


-- SQL 3 (Queries group)
-- Put some data in car2tariff table
INSERT INTO car2tariff (car_id, tariff_id)
    (SELECT cars.id, tariff.id
     FROM cars
            CROSS JOIN tariff
     WHERE cars.model = 'Lada'
       AND tariff.price_per_minute = 5)
UNION
    (SELECT cars.id, tariff.id
     FROM cars
            CROSS JOIN tariff
     WHERE cars.model = 'Camry'
       AND tariff.price_per_minute = 10)
UNION
    (SELECT cars.id, tariff.id
     FROM cars
            CROSS JOIN tariff
     WHERE (cars.model IN ('Bugatti', 'Lambo')
              AND tariff.price_per_minute = 50));

-- Put some data in rents table
INSERT INTO rents (id, user_id, car_id, tariff_id, started_at, finished_at)
    (SELECT nextval('rents_id_seq'),
            users.id,
            cars.id,
            car2tariff.tariff_id,
            (now() - interval '2 days') :: timestamp,
            (now() - interval '1 day') :: TIMESTAMP
     FROM users,
          cars
            LEFT JOIN car2tariff ON cars.id = car2tariff.car_id
     WHERE users.phone = '71111111113'
       AND cars.number = 'а123фф777')
UNION (SELECT nextval('rents_id_seq'),
              users.id,
              cars.id,
              car2tariff.tariff_id,
              (now() - interval '2 days') :: TIMESTAMP,
              null
       FROM users,
            cars
              LEFT JOIN car2tariff ON cars.id = car2tariff.car_id
       WHERE users.phone = '71111111116'
         AND cars.number = 'а125фф777')
UNION
    (SELECT nextval('rents_id_seq'),
            users.id,
            cars.id,
            car2tariff.tariff_id,
            (now() - interval '1 days') :: TIMESTAMP,
            null
     FROM users,
          cars
            LEFT JOIN car2tariff ON cars.id = car2tariff.car_id
     WHERE users.phone = '71111111118'
       AND cars.number = 'а124фф777')
UNION
    (SELECT nextval('rents_id_seq'),
            users.id,
            cars.id,
            car2tariff.tariff_id,
            (now() - interval '4 days') :: TIMESTAMP,
            (now() - interval '2 days')
     FROM users,
          cars
            LEFT JOIN car2tariff ON cars.id = car2tariff.car_id
     WHERE users.phone = '71111111121'
       AND cars.number = 'а127фф777');
-------------------------------------------------------------------------------------------

-- SQL 4
-- select number of users in each status
SELECT count(id), status
FROM users
GROUP BY status;

-- SQL 5
-- Average rent duration for each user
SELECT u.phone, avg(rents.finished_at - rents.started_at) as average_rent_duration
FROM rents
       LEFT JOIN users u on rents.user_id = u.id
WHERE rents.finished_at IS NOT NULL
GROUP BY u.phone;

-- SQL 6
-- Top 5 users with max cost of rent
SELECT u.phone, max(rents.cost) as max_cost_per_user
FROM rents
       LEFT JOIN users u on rents.user_id = u.id
GROUP BY u.phone
ORDER BY max_cost_per_user DESC
LIMIT 5;

-- SQL 7
-- total spent money on rents with Bugatti and Lada cars, for users, who spend more than 100 for such rents
SELECT u.phone, sum(rents.cost) as total_cost_per_user
FROM rents
       LEFT JOIN users u on rents.user_id = u.id
       LEFT JOIN cars c2 on rents.car_id = c2.id
WHERE c2.model IN ('Bugatti', 'Lada')
GROUP BY u.phone
HAVING sum(rents.cost) > 100;

-- SQL 8
-- select only second rent for some users with number 7111111111*
WITH rents_with_nth_val as (
  SELECT id, nth_value(id, 2) OVER (PARTITION BY user_id ORDER BY started_at) as second_rent_id
  FROM rents
)
  SELECT rents.*
  FROM rents
  LEFT JOIN users ON rents.user_id = users.id
  WHERE users.phone LIKE '7111111111%' AND rents.id IN (SELECT second_rent_id FROM rents_with_nth_val);

-- SQL 9
-- Select top 5 users with most average rent cost
SELECT DISTINCT user_id, avg_cost
FROM (SELECT id, user_id, avg(rents.cost) OVER (PARTITION BY user_id) as avg_cost FROM rents) as avg_rents
ORDER BY avg_cost DESC
LIMIT 5;

-- SQL 10
-- SELECT only last rent for each user with phone number like 7111111111* 
WITH last_rents as (
    SELECT id, user_id, last_value(id) OVER user_rents as last_rent_id
    FROM rents
    WINDOW user_rents as (PARTITION BY user_id ORDER BY started_at
      range between unbounded preceding and unbounded following)
    )
SELECT * FROM rents
LEFT JOIN users u on rents.user_id = u.id
WHERE u.phone LIKE '7111111111%' AND rents.id IN (
    select last_rent_id FROM last_rents
);
