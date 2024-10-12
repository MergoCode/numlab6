import math
import matplotlib.pyplot as plt

# Аналітична функція
def f(x):
    return math.sin(x)

def F(x):
    return -math.cos(x)

# Точне значення інтегралу
def exact_integral(a, b):
    return F(b) - F(a)

# Наближене значення інтегралу методом Сімпсона
def simpsons_rule(N, a, b):
    h = (b - a) / N
    Int_N = f(a) + f(b)

    for i in range(1, N):
        if (i % 2) == 0:
            Int_N += 2 * f(a + i * h)
        else:
            Int_N += 4 * f(a + i * h)

    Int_N *= (h / 3)
    return Int_N

# Адаптивний алгоритм
def adaptive_algorithm(a, b, eps):
    h = (b - a) / 2
    Int1 = (h / 3) * (f(a) + 4 * f(a + h) + f(b))
    Int2 = (h / 6) * (f(a) + 4 * f(a + h / 2) + f(a + h)) + \
            (h / 6) * (f(a + h) + 4 * f(a + (3 / 2) * h) + f(b))

    if math.fabs(Int2 - Int1) < eps:
        return Int2
    else:
        return adaptive_algorithm(a, a + h, eps) + adaptive_algorithm(a + h, b, eps)

# Метод Рунге-Ромберга
def runge_romberg(I_N0, I_N2, N0):
    return I_N2 + (I_N2 - I_N0) / 15

# Метод Ейткена
def aitken(N0, I_N0, I_N2, I_N4):
    return (I_N0 * I_N0 - I_N2 * I_N4) / (I_N2 - I_N0)

# Головна функція
def main():
    a = 0
    b = 10
    I_exact = exact_integral(a, b)
    print(f"Точне значення інтегралу: {I_exact}")

    # Дослідження точності методу Сімпсона
    N = 8
    eps_list = []
    N_values = []

    while N <= 50:  # Збільшити значення N для побудови графіка
        I_N = simpsons_rule(N, a, b)
        eps = abs(I_N - I_exact)
        eps_list.append(eps)
        N_values.append(N)
        N += 2

    # Побудова графіка
    plt.figure()
    plt.plot(N_values, eps_list, '-.')
    plt.xscale('log')
    plt.yscale('log')
    plt.title('Залежність похибки від числа вузлів N')
    plt.xlabel('Кількість вузлів N')
    plt.ylabel('Похибка ε')
    plt.grid()
    plt.show()

    # Знайдемо Nopt
    Nopt = N_values[eps_list.index(min(eps_list))]
    epsopt = abs(simpsons_rule(Nopt, a, b) - I_exact)
    print(f"Nopt = {Nopt}, epsopt = {epsopt}")

    # Визначаємо N0
    N0 = Nopt // 10 * 8  # Округляємо до найближчого кратного 8
    print(f"N0 = {N0}")

    # Похибка для N0
    eps0 = abs(simpsons_rule(N0, a, b) - I_exact)
    print(f"eps0 для N0 = {eps0}")

    # Уточнення значення інтегралу методом Рунге-Ромберга
    I_N0 = simpsons_rule(N0, a, b)
    I_N2 = simpsons_rule(N0 // 2, a, b)
    I_RR = runge_romberg(I_N0, I_N2, N0)
    epsR = abs(I_RR - I_exact)
    print(f"Уточнене значення інтегралу Рунге-Ромберга: {I_RR}, epsR = {epsR}")

    # Уточнення значення інтегралу методом Ейткена
    I_N4 = simpsons_rule(N0 // 4, a, b)
    I_Aitken = aitken(N0, I_N0, I_N2, I_N4)
    epsE = abs(I_Aitken - I_exact)
    print(f"Уточнене значення інтегралу Ейткена: {I_Aitken}, epsE = {epsE}")

    # Адаптивний алгоритм
    eps_adaptive = 1e-12
    I_adaptive = adaptive_algorithm(a, b, eps_adaptive)
    eps_adaptive_calc = abs(I_adaptive - I_exact)
    print(f"Значення інтегралу адаптивним алгоритмом: {I_adaptive}, похибка: {eps_adaptive_calc}")

if __name__ == "__main__":
    main()
