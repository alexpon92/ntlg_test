"""
Выведите на экран все уникальные гео-ID из значений словаря ids. Т. е. список вида [213, 15, 54, 119, 98, 35]

ids = {'user1': [213, 213, 213, 15, 213], 'user2': [54, 54, 119, 119, 119], 'user3': [213, 98, 98, 35]}
"""

ids = {'user1': [213, 213, 213, 15, 213], 'user2': [54, 54, 119, 119, 119], 'user3': [213, 98, 98, 35]}
unique_geo = None

for user, id_list in ids.items():
    if unique_geo is None:
        unique_geo = set(id_list)
    else:
        unique_geo = unique_geo.union(id_list)

print(unique_geo)
