"""
Задание 4 *

Дана статистика рекламных каналов по объемам продаж. Напишите скрипт,
который возвращает название канала с максимальным объемом.
Т. е. в данном примере скрипт должен возвращать 'yandex'.
stats = {'facebook': 55, 'yandex': 120, 'vk': 115, 'google': 99, 'email': 42, 'ok': 98}
"""

stats = {'facebook': 55, 'yandex': 120, 'vk': 115, 'google': 99, 'email': 42, 'ok': 98}

greatest_channel_ever = {'name': None, "value": None}

for channel, val in stats.items():
    if greatest_channel_ever["name"] is None or val > greatest_channel_ever["value"]:
        greatest_channel_ever["name"] = channel
        greatest_channel_ever["value"] = val

print(greatest_channel_ever["name"])
