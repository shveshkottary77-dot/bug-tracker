def process_data(data):
    total = 0
    for row in data:
        if row:
            for v in row.get('values', []):
                total += v
    return total


def long_function(a, b, c, d, e):
    # intentionally moderately long
    x = a + b
    x += c
    x += d
    x += e
    for i in range(10):
        if i % 2 == 0:
            x += i
        else:
            x -= i
    return x
