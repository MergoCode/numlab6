import math
import matplotlib.pyplot as plt
# Функції
def f(x):
    return math.sin(x)

def F(x):
    return -math.cos(x)
iter_count = 0
def I(N):
    N = int(N)
    a = 0
    b = 10
    h = (b - a) / N
    Int_N = f(a) + f(b)
    
    for i in range(1, N):
        if (i % 2) == 0:
            Int_N += 2 * f(a + i * h)
        else:
            Int_N += 4 * f(a + i * h)
    Int_N *= (h / 3)
    return Int_N

def Adapt_alg(a, b):
    eps = 1e-12
    global iter_count
    h = (b - a) / 2
    Int1 = h / 3 * (f(a) + 4 * f(a + h) + f(b))
    Int2 = h / 6 * (f(a) + 4 * f(a + h / 2) + f(a + h)) + h / 6 * (f(a + h) + 4 * f(a + (3 / 2) * h) + f(b))

    if math.fabs(Int2 - Int1)<eps:
        simp = Int2
    else:
        iter_count += 1
        simp = Adapt_alg(a, a+h) + Adapt_alg(a+h, b)
    return simp


def main():
    a = 0
    b = 10
    global iter_count
    I0 = F(b) - F(a)
    file1 = open("inE.txt", "w")
    file2 = open("inAdE.txt", "w")
    N = 8
    eps = 1e-12
    while True:
        N += 2
        epsI = math.fabs(I(N) - I0)
        file1.write(f"{N} {epsI:e}\n")
        if epsI <= 1e-10:
            break
    Nopt = N
    epsopt = math.fabs(I(Nopt) - I0)
    file1.write(f"Nopt = {Nopt} epsopt = {epsopt}\n")

    N0 = Nopt/10
    N0 -= N0 % 8
    N0 = int(N0)
    print(N0)
    file1.write(f"N0 = {N0}\n")

    eps0 = math.fabs(I(int(N0)) - I0)
    file1.write(f"eps0 = {eps0}\n")
    print(N0)
    Ir = I(N0) + (I(int(N0)) - I(int(N0/2))) / 15
    print(N0)
    file1.write(f"Ir = {Ir}\n")

    epsR = math.fabs(Ir - 10)
    file1.write(f"epsR = {epsR}\n")

    Ie = (I(int(N0 / 2))*I(int(N0 / 2)) - I(N0)*I(int(N0/4))) / (2*I(int(N0/2)) - (I(N0) + I(int(N0/4))))
    file1.write(f"Ie = {Ie}\n")

    p = (1/math.log(2)) * math.log(math.fabs((I(int(N0/4)) - I(N0/2))/(I(N0/2) - I(N0))))
    file1.write(f"p = {p}\n")

    epsE = math.fabs(Ie - I0)
    file1.write(f"epsE = {epsE}\n")

    Adapt_alg(a, b)

    file1.write(f"eps = {eps}\n Adapt_alg = {Adapt_alg(a, b)}\n iter = {iter_count}\n")
    eps = 1e-12
    while(eps <= 1e-2):
        iter_count = 0
        Adapt_alg(a, b)
        file2.write(f"{eps} {iter_count}\n")
        eps *= 1.5
    file1.close()
    file2.close()
    e_val = []
    N_val = []
    for N in range(10, 100, 10):
        N_val.append(N)
        e = abs(I(N) - I0)
        e_val.append(e)
    print(e_val)
    plt.figure(1)
    plt.plot(N_val, e_val, "--")
    plt.grid()
    plt.show()



main()
