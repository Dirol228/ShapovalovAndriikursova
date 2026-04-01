import random
import time
from fibonacci_core import fibonacci


def fibonacci_sequential(data):
    results = []
    for n in data:
        results.append(fibonacci(n))
    return results


def generate_input_data(size, min_n=50, max_n=65):
    return [random.randint(min_n, max_n) for _ in range(size)]


def measure_sequential_time(data, runs=20):
    total_time = 0.0

    for _ in range(runs):
        start_time = time.perf_counter()
        fibonacci_sequential(data)
        end_time = time.perf_counter()
        total_time += end_time - start_time

    return total_time / runs