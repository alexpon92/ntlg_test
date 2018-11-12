/*
        Написать запрос, который выводит общее число тегов
*/
print("tags count: ", db.tags.count());
/*
        Добавляем фильтрацию: считаем только количество тегов woman
*/
print("woman tags count: ", db.tags.find({name:{"$eq":"woman"}}).count());
/*
        Очень сложный запрос: используем группировку данных посчитать количество вхождений для каждого тега
        и напечатать top-3 самых популярных
*/
print("Aggregate by name with standard $groupby, print most rated top-3 tags names: ");
printjson(
        db.tags.aggregate(
          [
            {"$group":
              {
                "_id": "$name",
                "count": { $sum: 1 }
              }
            },
            { $sort: { count: -1 } },
            { $limit: 3}
          ]
        )['_batch']
);

/*
    Более короткий вариант с sortByCount
*/
print("Aggregate by name with short $sortByCount notation, print most rated top-3 tags names: ");
printjson(
  db.tags.aggregate(
    [
      { $sortByCount: "$name" },
      { $limit: 3 }
    ]
  )['_batch']
);
