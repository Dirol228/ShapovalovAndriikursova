import time
from multiprocessing import Pool, cpu_count
from fibonacci_core import fibonacci


def split_into_chunks(data, chunk_count):
    chunk_size = len(data) // chunk_count
    remainder = len(data) % chunk_count

    chunks = []
    start = 0

    for i in range(chunk_count):
        extra = 1 if i < remainder else 0
        end = start + chunk_size + extra
        chunks.append(data[start:end])
        start = end

    return chunks


def process_chunk(chunk):
    results = []
    for n in chunk:
        results.append(fibonacci(n))
    return results


def fibonacci_parallel(data, processes=None, chunks_per_process=8):
    if processes is None:
        processes = cpu_count()

    chunk_count = processes * chunks_per_process
    chunks = split_into_chunks(data, chunk_count)

    with Pool(processes=processes) as pool:
        chunk_results = pool.map(process_chunk, chunks)

    results = []
    for part in chunk_results:
        results.extend(part)

    return results


def fibonacci_parallel_with_pool(data, pool, processes, chunks_per_process=8):
    chunk_count = processes * chunks_per_process
    chunks = split_into_chunks(data, chunk_count)

    chunk_results = pool.map(process_chunk, chunks)

    results = []
    for part in chunk_results:
        results.extend(part)

    return results


def measure_parallel_time(data, runs=20, processes=None, chunks_per_process=8):
    if processes is None:
        processes = cpu_count()

    total_time = 0.0

    with Pool(processes=processes) as pool:
        fibonacci_parallel_with_pool(data[:1000], pool, processes, chunks_per_process)

        for _ in range(runs):
            start_time = time.perf_counter()
            fibonacci_parallel_with_pool(data, pool, processes, chunks_per_process)
            end_time = time.perf_counter()
            total_time += end_time - start_time

    return total_time / runs