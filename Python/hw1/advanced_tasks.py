"""
В переменных a и b записаны 2 различных числа.
Вам необходимо написать код, который меняет значения a и b местами без использования третьей переменной.
"""
first_val = 123
sec_val = 5661

# standard XOR algorithm is used
first_val = first_val ^ sec_val
sec_val = sec_val ^ first_val
first_val = first_val ^ sec_val

print(first_val, sec_val)

"""
Дано число в двоичной системе счисления: num=10011. Напишите алгоритм перевода этого числа в привычную 
нам десятичную систему счисления.
Возможно, вам понадобится цикл прохождения всех целых чисел от 0 до m:
for n in range(m)
"""
num = 10011

# handmade algorithm
num = str(num)[::-1]
res = 0

for n in range(len(num)):
    res += int(num[n]) * 2 ** (int(n))

print(res)
