import math
import matplotlib.pyplot as plt
# Функції
def f(x):
    return math.sin(x)

def F(x):
    return -math.cos(x)

def I(N):
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

def Adapt_alg(a, b, eps):
    iter_count = 0
    h = (b - a) / 2
    Int1 = h / 3 * (f(a) + 4 * f(a + h) + f(b))
    Int2 = h / 6 * (f(a) + 4 * f(a + h / 2) + f(a + h)) + h / 6 * (f(a + h) + 4 * f(a + (3 / 2) * h) + f(b))

    if math.fabs(Int2 - Int1) < eps:
        return Int2, iter_count
    else:
        iter_count += 1
        left_result, left_iter = Adapt_alg(a, a + h, eps)
        right_result, right_iter = Adapt_alg(a + h, b, eps)
        iter_count += left_iter + right_iter
        return left_result + right_result, iter_count

def main():
    a = 0
    b = 10
    eps = 1e-5
    iter_count = 0
    I_exact = F(b) - F(a)
    # Запис результатів у файл
    with open("inE.txt", "wt") as file1, open("inAdE.txt", "wt") as file2:
        # Метод Сімпсона
        eps_values = []
        iter_values = []
        
        N = 8
        epsI = 0
        
        while True:
            N += 2
            epsI = math.fabs(I(N) - I_exact)
            file1.write(f"{N} {epsI:e}\n")
            if epsI <= 1e-10:
                break

        Nopt = N
        epsopt = math.fabs(I(Nopt) - I_exact)

        file1.write(f"Nopt = {Nopt} \t epsopt = {epsopt:e}\n")

        N0 = Nopt // 10
        N0 = N0 - N0 % 8
        file1.write(f"N0 = {N0}\n")
        eps0 = math.fabs(I(N0) - I_exact)
        file1.write(f"eps0 = {eps0:e}\n")

        Ir = I(N0) + (I(N0) - I(N0 // 2)) / 15
        file1.write(f"Ir = {Ir:f}\n")
        epsR = math.fabs(Ir - I_exact)
        file1.write(f"epsR = {epsR:e}\n")
        Ie = (I(N0 // 2) ** 2 - I(N0) * I(N0 // 4)) / (2 * I(N0 // 2) - (I(N0) + I(N0 // 4)))
        file1.write(f"Ie = {Ie:f}\n")
        p = (1 / math.log(2)) * math.log(math.fabs((I(N0 // 4) - I(N0 // 2)) / (I(N0 // 2) - I(N0))))
        file1.write(f"p = {p:f}\n")
        epsE = math.fabs(Ie - I_exact)
        file1.write(f"epsE = {epsE:e}\n")

        # Запис результатів адаптивного алгоритму
        total_integral, iter_count = Adapt_alg(a, b, eps)
        file1.write(f"eps = {epsE:e} Adapt_alg = {total_integral:f} iter = {iter_count}\n")
        # Цикл для різних значень eps
        eps = 1e-12
        while eps <= 1e-2:
            print(iter_count)
            iter_count = 0
            Adapt_alg(a, b, eps)
            file2.write(f"{eps:e} {iter_count}\n")
            eps_values.append(eps)
            iter_values.append(iter_count)
            eps *= 1.5
        print(f"eps: {eps}, iterations: {iter_count}")
        print(iter_values)
    # Побудова графіку
    plt.plot(eps_values, iter_values, linestyle="-")
    plt.xscale('log')
    plt.xlabel('eps')
    plt.ylabel('iterations')
    plt.title('Adapt_alg iterations depending on eps')
    plt.grid(True)
    plt.show()

main()
