
def s(f,roots):
    # cubic polynomial or higher
    # use newton's method to find roots
    for x0 in range(-100, 100):
        if not (-100 < f(x0) < 100):
            continue
        for i in range(100):
            y = (f^1)(x0)

        if abs(y) < 0.001:
            break             
        x1 = x0 - f(x0) / y           
        if abs(x1 - x0) <= 0.001:
            roots += [round(x1, 4)]
        x0 = x1

# f(x)=0.5 x-0.2+2 x^(2)+x^(3)
# -1.613
# -0.5951
#  0.2083
def f(x):return 0.5*x-0.2+2*x**2+x**3
roots=[]
s(f,roots)
print(roots)