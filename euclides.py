def euclides_mdc(dividendo, divisor):
    while divisor != 0:
        temp = divisor
        divisor = dividendo % divisor
        dividendo = temp    
    return dividendo
