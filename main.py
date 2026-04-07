import time
from multiprocessing import Pool, cpu_count


def fib_fast_doubling(n: int) -> int:


    def helper(k: int) -> tuple[int, int]:
        if k == 0:
            return 0, 1

        a, b = helper(k // 2)
        c = a * (2 * b - a)
        d = a * a + b * b

        if k % 2 == 0:
            return c, d
        return d, c + d

    return helper(n)[0]


def fibonacci_sequence_sequential(n: int) -> list[int]:

    return [fib_fast_doubling(i) for i in range(n + 1)]


def fibonacci_sequence_parallel_with_pool(n: int, pool: Pool) -> list[int]:

    indices = list(range(n + 1))
    return pool.map(fib_fast_doubling, indices)


def measure_sequential_time(n: int, runs: int = 3) -> float:
    total = 0.0
    for _ in range(runs):
        t0 = time.perf_counter()
        fibonacci_sequence_sequential(n)
        total += time.perf_counter() - t0
    return total / runs


def measure_parallel_time(n: int, runs: int = 3, processes: int | None = None) -> float:
    if processes is None:
        processes = cpu_count()

    total = 0.0
    with Pool(processes=processes) as pool:
        pool.map(fib_fast_doubling, list(range(1000)))  # прогрів пулу

        for _ in range(runs):
            t0 = time.perf_counter()
            fibonacci_sequence_parallel_with_pool(n, pool)
            total += time.perf_counter() - t0

    return total / runs


def verify_parallel_algorithm() -> None:
    print("ВЕРИФІКАЦІЯ ПАРАЛЕЛЬНОГО АЛГОРИТМУ")
    print("-" * 80)

    test_values = [100, 1000, 5000, 10000]

    for n in test_values:
        seq = fibonacci_sequence_sequential(n)
        with Pool(processes=4) as pool:
            par = fibonacci_sequence_parallel_with_pool(n, pool)

        if seq == par:
            print(f"Результати збігаються для n = {n}.")
        else:
            print(f"Виявлено розбіжності для n = {n}. ПОМИЛКА!")

    print()


def run_table_2_2() -> None:
    print("ТАБЛИЦЯ 2.2 – СЕРЕДНІЙ ЧАС ВИКОНАННЯ ПОСЛІДОВНОГО АЛГОРИТМУ")
    print("-" * 90)
    print(f"{'Значення n':<20}{'Кількість прогонів':<25}{'Середній час виконання, с':<30}")
    print("-" * 90)

    values_n = [10000, 20000, 30000, 40000, 50000, 60000]

    for n in values_n:
        avg_time = measure_sequential_time(n, runs=3)
        print(f"{n:<20}{3:<25}{avg_time:<30.6f}")

    print("-" * 90)
    print()


def run_table_5_1(processes: int = 8) -> None:
    print("ТАБЛИЦЯ 5.1")
    print("-" * 110)
    print(
        f"{'Значення n':<20}"
        f"{'Послідовний час, с':<30}"
        f"{'Паралельний час, с':<30}"
        f"{'Прискорення':<20}"
    )
    print("-" * 110)

    values_n = [10000, 20000, 30000, 40000, 50000, 60000]

    for n in values_n:
        seq_time = measure_sequential_time(n, runs=3)
        par_time = measure_parallel_time(n, runs=3, processes=processes)
        speedup = seq_time / par_time

        print(
            f"{n:<20}"
            f"{seq_time:<30.6f}"
            f"{par_time:<30.6f}"
            f"{speedup:<20.6f}"
        )

    print("-" * 110)
    print()


def run_table_5_2() -> None:
    print("ТАБЛИЦЯ 5.2")
    print("-" * 95)
    print(
        f"{'Значення n':<20}"
        f"{'Кількість процесів':<25}"
        f"{'Паралельний час, с':<25}"
        f"{'Прискорення':<15}"
    )
    print("-" * 95)

    n = 60000
    process_counts = [2, 4, 6, 8]

    seq_time = measure_sequential_time(n, runs=3)

    for processes in process_counts:
        par_time = measure_parallel_time(n, runs=3, processes=processes)
        speedup = seq_time / par_time

        print(
            f"{n:<20}"
            f"{processes:<25}"
            f"{par_time:<25.6f}"
            f"{speedup:<15.6f}"
        )

    print("-" * 95)
    print()


if __name__ == "__main__":
    verify_parallel_algorithm()
    run_table_2_2()
    run_table_5_1(processes=8)
    run_table_5_2()