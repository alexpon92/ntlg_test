#/bin/sh
RED='\033[0;31m'
NC='\033[0m'
KW_PATH='/data/keywords.csv'
SAVE_PATH='/data/top_rated.csv'

echo -e "\nFIO: Ponomarev Alexander\n"
echo -e "----------------\nETL homework \n----------------"
echo "EXTRACT. Creating \"keywords\" table and load data from ${KW_PATH}"

if [ ! -f /data/keywords.csv ]; then
    echo -e "${RED}Keywords data source is not found in path ${KW_PATH}${NC}"
    exit
fi

echo -e "\nCreating table keywords..."
psql --host $APP_POSTGRES_HOST  -U postgres -c \
    "DROP TABLE IF EXISTS keywords"

psql --host $APP_POSTGRES_HOST -U postgres -c \
  "CREATE TABLE keywords (
    movieId bigint,
    tags text
  );"
echo -e "\nCreated"

echo -e "\nLoading data from ${KW_PATH}..."
COPY_RES=$(psql --host $APP_POSTGRES_HOST -U postgres -c \
  "\\COPY keywords FROM '/${KW_PATH}/' DELIMITER ',' CSV HEADER" | grep -Eo '[0-9]+')
echo "Copied from file: ${COPY_RES}"

echo -e "\nData is loaded. Checking data consistency..."
SELECT_RES=$(psql --host $APP_POSTGRES_HOST -U postgres -c \
  "SELECT COUNT(*) FROM keywords;" | grep -Eo '[0-9]+')

echo "Counted in DB: ${SELECT_RES}"

echo -e "\n---------------\n"
echo -e "TRANSFORM AND LOAD\n"

echo "Creating table top_rated_tags and uploading data"
psql --host $APP_POSTGRES_HOST  -U postgres -c \
    "DROP TABLE IF EXISTS top_rated_tags"

echo -e "\nUploading data to top_rated_tags table"
psql --host $APP_POSTGRES_HOST -U postgres -c \
  "WITH top_rated as (
    SELECT movieid, avg(rating) as avg_rating
    FROM ratings
    GROUP BY movieid
    HAVING count(userid) > 50
    ORDER BY avg_rating DESC, movieid ASC
    LIMIT 150
)
SELECT top_rated.movieid, top_rated.avg_rating, keywords.tags INTO top_rated_tags
FROM top_rated
   LEFT JOIN keywords ON top_rated.movieid = keywords.movieid
WHERE keywords.movieid IS NOT NULL"

echo -e "\nUploading data to ${SAVE_PATH}"
psql --host $APP_POSTGRES_HOST -U postgres -c \
  "\\copy (SELECT * FROM top_rated_tags) TO '${SAVE_PATH}' With CSV DELIMITER E'\t'"

echo -e "\n"
