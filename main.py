import time
from datetime import datetime


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


if __name__ == "__main__":
    alpha_input = int(input("Введіть генератор групи G (α) : "))
    beta_input = int(input("Введіть елемент групи G (β) : "))
    n_input = int(input("Введіть порядок групи G (n) : "))

    time_limit_input = 10 * 60  # 10 хвилин у секундах
    start = datetime.now()
    result_output, execution_time_output = discrete_log(alpha_input, beta_input, n_input, time_limit_input)
    stop = datetime.now()
    print(f"Час виконання алгоритму: {stop - start}")
    if result_output != -1:
        print("Дискретний логарифм:", result_output)
    else:
        print("Дискретний логарифм не знайдено. Завершено за {} секунд.".format(execution_time_output))
