import time
from multiprocessing import Pool, cpu_count

def factorize_single_number(number):
    factors = []
    for i in range(1, number + 1):
        if number % i == 0:
            factors.append(i)
    return factors

def factorize(*numbers):
    return [factorize_single_number(num) for num in numbers]

def measure_time_sync(*numbers):
    start_time = time.time()
    result = factorize(*numbers)
    end_time = time.time()
    elapsed_time = end_time - start_time
    return result, elapsed_time

def factorize_parallel(number):
    return factorize_single_number(number)

def measure_time_parallel(*numbers):
    start_time = time.time()

    with Pool(cpu_count()) as pool:
        result = pool.map(factorize_parallel, numbers)

    end_time = time.time()
    elapsed_time = end_time - start_time
    return result, elapsed_time

if __name__ == '__main__':
    result_sync, time_sync = measure_time_sync(128, 255, 99999, 10651060)
    result_parallel, time_parallel = measure_time_parallel(128, 255, 99999, 10651060)

    a_sync, b_sync, c_sync, d_sync = result_sync
    a_parallel, b_parallel, c_parallel, d_parallel = result_parallel

    assert a_sync == [1, 2, 4, 8, 16, 32, 64, 128]
    assert b_sync == [1, 3, 5, 15, 17, 51, 85, 255]
    assert c_sync == [1, 3, 9, 41, 123, 271, 369, 813, 2439, 11111, 33333, 99999]
    assert d_sync == [1, 2, 4, 5, 7, 10, 14, 20, 28, 35, 70, 140, 76079, 152158, 304316, 380395, 532553, 760790, 1065106, 1521580, 2130212, 2662765, 5325530, 10651060]

    print("Synchronous results:")
    print("a:", a_sync)
    print("b:", b_sync)
    print("c:", c_sync)
    print("d:", d_sync)
    print("Elapsed time (sync):", time_sync)

    print("\nParallel results:")
    print("a:", a_parallel)
    print("b:", b_parallel)
    print("c:", c_parallel)
    print("d:", d_parallel)
    print("Elapsed time (parallel):", time_parallel)
