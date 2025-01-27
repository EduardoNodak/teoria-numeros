def extendedEuclides(a,b):
    if b==0:
        return [1,0,a]
    else:
        x,y,d=extendedEuclides(b, a%b)
        return [y,x-(a//b)*y,d]
