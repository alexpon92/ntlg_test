CREATE TABLE IF NOT EXISTS links_odd
(
  CHECK (movieid % 2 = 1)
)
  INHERITS (links);

CREATE TABLE IF NOT EXISTS links_even
(
  CHECK (movieid % 2 = 0)
)
  INHERITS (links);


CREATE RULE insert_links_with_even_movieid AS ON INSERT
  TO links WHERE movieid % 2 = 0 DO INSTEAD INSERT INTO links_even
                                    VALUES (NEW.*);

CREATE RULE insert_links_with_odd_movieid AS ON INSERT
  TO links WHERE movieid % 2 = 1 DO INSTEAD INSERT INTO links_odd
                                    VALUES (NEW.*);
