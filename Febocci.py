def Fibocci(n):
    sequence = []
    a, b = 0, 1
    for _ in range(n):
        sequence.append(a)
        a, b = b, a + b
    return sequence

fibocci_num = Fibocci(100)
print(fibocci_num)