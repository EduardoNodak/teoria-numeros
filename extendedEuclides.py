def extendedEuclides(a, b): 
    if a == 0:
        return b, 0, 1
    mdc, x1, y1 = euclides(b % a, a)
    x = y1 - (b // a) * x1
    y = x1
    return mdc, x, y
