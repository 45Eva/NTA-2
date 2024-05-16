import time
from datetime import datetime
import sympy


def discrete_log(alpha_arg, beta_arg, n_arg, time_limit_arg):
    start_time = time.time()
    for i in range(n_arg):
        result = pow(alpha_arg, i, n_arg + 1)
        end_time = time.time()
        execution_time = end_time - start_time
        if result == beta_arg:
            return i, execution_time
        if execution_time > time_limit_arg:
            return -1, execution_time


def canonical_decomposition(n):
    """
    Обчислює канонічний розклад числа n.

    Параметри:
    - n: ціле число

    Повертає:
    - factors: словник, де ключі - прості числа, а значення - їх потужності в розкладі n
    """
    factors = sympy.factorint(n)
    return factors


def build_tables(alpha, n, factors):
    """
    Будує таблиці для значень r_(p,j) = α^((n*j)/p) для кожного простого множника числа n.

    Параметри:
    - alpha: генератор групи G
    - n: порядок групи G
    - factors: канонічний розклад числа n

    Повертає:
    - tables: словник, де ключі - прості множники числа n, а значення - таблиці значень r_(p,j)
    """
    tables = {}
    for prime, power in factors.items():
        for i in range(power):
            temp = []
            for j in range(prime):
                r_p_i = pow(alpha, (n * j // prime), n + 1)  # Обчислення значення r_{(p,i)}
                temp.append(r_p_i)
        tables[prime] = temp
    return tables


def compute_x_i(n, prime, alpha, beta, power, u):
    x = u.index(pow(beta, int(n / prime), n + 1))
    num = x
    for i in range(1, power):
        alpha_st = pow(alpha, num, n + 1)
        m = beta * pow(alpha_st, -1, n + 1)
        p = int(n / prime ** (i + 1))
        rish = pow(m, p, n + 1)
        our_rish = u.index(rish)
        num = num + (our_rish * prime ** i)
        x = (x + our_rish * prime ** i) % prime ** power
    mod = prime ** power
    return x, mod


def chinese_remainder_theorem(congruences):
    """
    Застосовує китайську теорему про лишки для розв'язку системи конгруенцій.

    Параметри:
    - congruences: список кортежів (y_i, modulus_i), де y_i - залишок, modulus_i - модуль

    Повертає:
    - solution: розв'язок системи конгруенцій
    """
    M = 1
    for _, modulus in congruences:
        M *= modulus

    solution = 0
    for y_i, modulus_i in congruences:
        M_i = (M // modulus_i)
        inversed_M_i = pow(M_i, -1, modulus_i)
        solution += y_i * M_i * inversed_M_i
        solution %= M

    return solution % M


def silver_polig_hellman(alpha, beta, n):
    factors = canonical_decomposition(n)
    tables = build_tables(alpha, n, factors)

    congruences = []
    for prime in factors:
        x_i = compute_x_i(n, prime, alpha, beta, factors[prime], tables[prime])
        congruences.append(x_i)
    x = chinese_remainder_theorem(congruences)
    return x


if __name__ == "__main__":
    alpha_input = int(input("Введіть генератор групи G (α) : "))
    beta_input = int(input("Введіть елемент групи G (β) : "))
    n_input = int(input("Введіть порядок групи G (n) : "))

    time_limit_input = 10 * 60  # 10 хвилин у секундах
    start = datetime.now()
    result_output, execution_time_output = discrete_log(alpha_input, beta_input, n_input, time_limit_input)
    stop = datetime.now()
    print(f"Час виконання алгоритму дискретного перебору : {stop - start}")
    if result_output != -1:
        print("Дискретний логарифм:", result_output)
    else:
        print("Дискретний логарифм не знайдено. Завершено за {} секунд.".format(execution_time_output))

    start = datetime.now()
    # Виклик функції алгоритму СПГ
    x = silver_polig_hellman(alpha_input, beta_input, n_input)
    stop = datetime.now()
    print(f"Час виконання алгоритму СПГ : {stop - start}")
    print("x =", x)