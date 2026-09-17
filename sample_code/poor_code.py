def bad(a,b,c,d,e,f,g):
    x=0
    for i in range(10):
        if a:
            if b:
                if c:
                    if d:
                        x += i
    return x


def duplicate_one(a):
    s = 0
    for i in range(len(a)):
        s += a[i]
    return s


def duplicate_two(b):
    s = 0
    for i in range(len(b)):
        s += b[i]
    return s
