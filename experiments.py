from sequential import (
    fibonacci_sequential,
    generate_input_data,
    measure_sequential_time,
)
from parallel import fibonacci_parallel, measure_parallel_time


def verify_parallel_algorithm():
    print("ВЕРИФІКАЦІЯ ПАРАЛЕЛЬНОГО АЛГОРИТМУ")
    print("-" * 75)

    data = generate_input_data(150000, 50, 65)

    sequential_result = fibonacci_sequential(data)
    parallel_result = fibonacci_parallel(data, processes=8, chunks_per_process=8)

    if sequential_result == parallel_result:
        print("Результати збігаються для набору з 150000 значень.")
        print("Паралельний алгоритм працює коректно.\n")
    else:
        print("Виявлено розбіжності в результатах!\n")


def run_table_5_1(processes=8, chunks_per_process=8):
    sizes = [1000000, 1200000, 1400000, 1600000, 1800000, 1900000, 2000000]

    print("ТАБЛИЦЯ 5.1")
    print("-" * 110)
    print(f"{'Кількість значень':<20}{'Діапазон n':<15}{'Послідовний час, с':<25}{'Паралельний час, с':<25}{'Прискорення':<15}")
    print("-" * 110)

    for size in sizes:
        data = generate_input_data(size, 50, 65)

        seq_time = measure_sequential_time(data, runs=20)
        par_time = measure_parallel_time(data, runs=20, processes=processes, chunks_per_process=chunks_per_process)
        speedup = seq_time / par_time

        print(f"{size:<20}{'50-65':<15}{seq_time:<25.6f}{par_time:<25.6f}{speedup:<15.6f}")


def run_table_5_2():
    size = 2000000
    process_counts = [2, 4, 6, 8]
    chunks_per_process = 8

    print("\nТАБЛИЦЯ 5.2")
    print("-" * 95)
    print(f"{'Кількість значень':<20}{'Кількість процесів':<25}{'Паралельний час, с':<25}{'Прискорення':<15}")
    print("-" * 95)

    data = generate_input_data(size, 50, 65)
    seq_time = measure_sequential_time(data, runs=20)

    for processes in process_counts:
        par_time = measure_parallel_time(data, runs=20, processes=processes, chunks_per_process=chunks_per_process)
        speedup = seq_time / par_time
        print(f"{size:<20}{processes:<25}{par_time:<25.6f}{speedup:<15.6f}")