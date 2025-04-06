import cmath
import math
from multiprocessing import Pool, cpu_count

def is_prime(n):
    if n < 2:
        return False
    for i in range(2, int(math.sqrt(n)) + 1):
        if n % i == 0:
            return False
    return True

def factorize(n):
    factors = []
    d = 2
    while n > 1:
        while n % d == 0:
            factors.append(d)
            n //= d
        d += 1 if d == 2 else 2
        if d * d > n:
            if n > 1:
                factors.append(n)
            break
    return factors

def operator_amplitude(args):
    n_max, operator = args
    a, l, m, p = operator
    amplitude = [0] * (n_max + 1)
    x_max = int(math.sqrt(n_max / a)) + 2
    marked_primes = set()
    for x in range(1, x_max):
        n = a * x**2 - l * x + m
        if 0 <= n <= n_max:
            p_base = 90 * n + (1 if p == 0 else p)
            if is_prime(p) and p * p == p_base and p not in marked_primes:
                amplitude[n] += 1
                marked_primes.add(p)
            elif not (is_prime(p) and p * p == p_base):
                amplitude[n] += 1
            p_x = p + 90 * (x - 1) if p != 0 else 0
            for i in range(1, (n_max - n) // p_x + 1) if p_x > 0 else []:
                n_new = n + i * p_x
                if n_new <= n_max:
                    amplitude[n_new] += 1
    return amplitude

def mark_composites(n_max, operators_dict, coprime_24):
    amplitude = {k: [0] * (n_max + 1) for k in coprime_24}
    with Pool(cpu_count()) as pool:
        for k in coprime_24:
            results = pool.map(operator_amplitude, [(n_max, op) for op in operators_dict[k]])
            for amp in results:
                for n in range(n_max + 1):
                    amplitude[k][n] += amp[n]
    return amplitude

def compute_primes_and_largest(n_max, amplitude, coprime_24, limit=10**9):
    total_primes = 0
    largest_prime = {k: 0 for k in coprime_24}
    seen_primes = set()
    for k in coprime_24:
        for n in range(n_max + 1):
            p = 90 * n + 1 if k == 1 else 90 * n + k
            if p <= limit and p not in seen_primes and amplitude[k][n] == 0:
                total_primes += 1
                seen_primes.add(p)
                largest_prime[k] = p
    return total_primes, largest_prime
operators = {
    7: [
        (90, 82, -1, 7), (90, 82, -1, 91), (90, 118, 37, 19), (90, 118, 37, 43),
        (90, 82, 17, 37), (90, 82, 17, 61), (90, 28, 2, 73), (90, 28, 2, 79),
        (90, 152, 64, 11), (90, 152, 64, 17), (90, 98, 25, 29), (90, 98, 25, 53),
        (90, 62, 9, 47), (90, 62, 9, 71), (90, 8, 0, 83), (90, 8, 0, 89),
        (90, 118, 35, 13), (90, 118, 35, 49), (90, 82, 15, 31), (90, 82, 15, 67),
        (90, 98, 23, 23), (90, 98, 23, 59), (90, 62, 7, 41), (90, 62, 7, 77)
    ],
    11: [
        (90, 120, 34, 7), (90, 120, 34, 53), (90, 132, 48, 19), (90, 132, 48, 29),
        (90, 120, 38, 17), (90, 120, 38, 43), (90, 90, 11, 13), (90, 90, 11, 77),
        (90, 78, -1, 11), (90, 78, -1, 91), (90, 108, 32, 31), (90, 108, 32, 41),
        (90, 90, 17, 23), (90, 90, 17, 67), (90, 72, 14, 49), (90, 72, 14, 59),
        (90, 60, 4, 37), (90, 60, 4, 83), (90, 60, 8, 47), (90, 60, 8, 73),
        (90, 48, 6, 61), (90, 48, 6, 71), (90, 12, 0, 79), (90, 12, 0, 89)
    ],
    13: [
        (90, 76, -1, 13), (90, 76, -1, 91), (90, 94, 18, 19), (90, 94, 18, 67),
        (90, 94, 24, 37), (90, 94, 24, 49), (90, 76, 11, 31), (90, 76, 11, 73),
        (90, 86, 6, 11), (90, 86, 6, 83), (90, 104, 29, 29), (90, 104, 29, 47),
        (90, 86, 14, 23), (90, 86, 14, 71), (90, 86, 20, 41), (90, 86, 20, 53),
        (90, 104, 25, 17), (90, 104, 25, 59), (90, 14, 0, 77), (90, 14, 0, 89),
        (90, 94, 10, 7), (90, 94, 10, 79), (90, 76, 15, 43), (90, 76, 15, 61)
    ],
    17: [
        (90, 72, -1, 17), (90, 72, -1, 91), (90, 108, 29, 19), (90, 108, 29, 53),
        (90, 72, 11, 37), (90, 72, 11, 71), (90, 18, 0, 73), (90, 18, 0, 89),
        (90, 102, 20, 11), (90, 102, 20, 67), (90, 138, 52, 13), (90, 138, 52, 29),
        (90, 102, 28, 31), (90, 102, 28, 47), (90, 48, 3, 49), (90, 48, 3, 83),
        (90, 78, 8, 23), (90, 78, 8, 79), (90, 132, 45, 7), (90, 132, 45, 41),
        (90, 78, 16, 43), (90, 78, 16, 59), (90, 42, 4, 61), (90, 42, 4, 77)
    ],
    19: [
        (90, 70, -1, 19), (90, 70, -1, 91), (90, 106, 31, 37),                      #37, 73, 53, 17
        (90, 34, 3, 73), (90, 110, 27, 11), (90, 110, 27, 59),
        (90, 110, 33, 29), (90, 110, 33, 41), (90, 56, 6, 47), (90, 56, 6, 77),
        (90, 74, 5, 23), (90, 74, 5, 83), (90, 124, 40, 13), (90, 124, 40, 43),
        (90, 70, 7, 31), (90, 70, 7, 79), (90, 70, 13, 49), (90, 70, 13, 61),
        (90, 106, 21, 7), (90, 106, 21, 67), (90, 20, 0, 71), (90, 20, 0, 89),
        (90, 74, 15, 53), (90, 146, 59, 17), 
    ],
    23: [
        (90, 66, -1, 23), (90, 66, -1, 91), (90, 84, 10, 19), (90, 84, 10, 77),
        (90, 84, 18, 37), (90, 84, 18, 59), (90, 66, 9, 41), (90, 66, 9, 73),
        (90, 126, 41, 11), (90, 126, 41, 43), (90, 144, 56, 7), (90, 144, 56, 29),
        (90, 54, 5, 47), (90, 54, 5, 79), (90, 36, 2, 61), (90, 36, 2, 83),
        (90, 96, 16, 13), (90, 96, 16, 71), (90, 96, 24, 31), (90, 96, 24, 53),
        (90, 114, 33, 17), (90, 114, 33, 49), (90, 24, 0, 67), (90, 24, 0, 89)
    ],
    29: [
        (90, 60, -1, 29), (90, 60, -1, 91), (90, 150, 62, 11), (90, 150, 62, 19),
        (90, 96, 25, 37), (90, 96, 25, 47), (90, 24, 1, 73), (90, 24, 1, 83),
        (90, 144, 57, 13), (90, 144, 57, 23), (90, 90, 20, 31), (90, 90, 20, 59),
        (90, 90, 22, 41), (90, 90, 22, 49), (90, 36, 3, 67), (90, 36, 3, 77),
        (90, 156, 67, 7), (90, 156, 67, 17), (90, 84, 19, 43), (90, 84, 19, 53),
        (90, 30, 0, 61), (90, 30, 0, 89), (90, 30, 2, 71), (90, 30, 2, 79)
    ],
    31: [
        (90, 58, -1, 31), (90, 58, -1, 91), (90, 112, 32, 19), (90, 112, 32, 49),   #79, 61, 11, 29
        (90, 130, 45, 13), (90, 130, 45, 37), (90, 40, 4, 67), (90, 40, 4, 73),
        (90, 158, 69, 11), (90, 122, 41, 29),
        (90, 50, 3, 47), (90, 50, 3, 83), (90, 140, 54, 17), (90, 140, 54, 23),
        (90, 68, 10, 41), (90, 68, 10, 71), (90, 32, 0, 59), (90, 32, 0, 89),
        (90, 50, 5, 53), (90, 50, 5, 77), (90, 130, 43, 7), (90, 130, 43, 43),
        (90, 58, 9, 61), (90, 22, 1, 79)
    ],
    37: [
        (90, 52, -1, 37), (90, 52, -1, 91), (90, 88, 13, 19), (90, 88, 13, 73),
        (90, 92, 11, 11), (90, 92, 11, 77), (90, 128, 45, 23), (90, 128, 45, 29),
        (90, 92, 23, 41), (90, 92, 23, 47), (90, 38, 2, 59), (90, 38, 2, 83),
        (90, 88, 9, 13), (90, 88, 9, 79), (90, 142, 54, 7), (90, 142, 54, 31),
        (90, 88, 21, 43), (90, 88, 21, 49), (90, 52, 7, 61), (90, 52, 7, 67),
        (90, 92, 15, 17), (90, 92, 15, 71), (90, 38, 0, 53), (90, 38, 0, 89)
    ],
    41: [
        (90, 48, -1, 41), (90, 48, -1, 91), (90, 42, 0, 49), (90, 42, 0, 89),
        (90, 102, 24, 19), (90, 102, 24, 59), (90, 120, 39, 23), (90, 120, 39, 37),
        (90, 108, 25, 11), (90, 108, 25, 61), (90, 72, 7, 29), (90, 72, 7, 79),
        (90, 90, 22, 43), (90, 90, 22, 47), (90, 150, 62, 13), (90, 150, 62, 17),
        (90, 78, 12, 31), (90, 78, 12, 71), (90, 30, 2, 73), (90, 30, 2, 77),
        (90, 60, 9, 53), (90, 60, 9, 67), (90, 90, 6, 7), (90, 90, 6, 83)
    ],
    43: [
        (90, 46, -1, 43), (90, 46, -1, 91), (90, 154, 65, 7), (90, 154, 65, 19),
        (90, 64, 6, 37), (90, 64, 6, 79), (90, 46, 5, 61), (90, 46, 5, 73),
        (90, 116, 32, 11), (90, 116, 32, 53), (90, 134, 49, 17), (90, 134, 49, 29),
        (90, 44, 0, 47), (90, 44, 0, 89), (90, 26, 1, 71), (90, 26, 1, 83),
        (90, 136, 50, 13), (90, 136, 50, 31), (90, 64, 10, 49), (90, 64, 10, 67),
        (90, 116, 36, 23), (90, 116, 36, 41), (90, 44, 4, 59), (90, 44, 4, 77)
    ],
    47: [
        (90, 42, -1, 47), (90, 42, -1, 91), (90, 78, 5, 19), (90, 78, 5, 83),
        (90, 132, 46, 11), (90, 132, 46, 37), (90, 78, 11, 29), (90, 78, 11, 73),
        (90, 108, 26, 13), (90, 108, 26, 59), (90, 72, 8, 31), (90, 72, 8, 77),
        (90, 108, 30, 23), (90, 108, 30, 49), (90, 102, 17, 7), (90, 102, 17, 71),
        (90, 48, 0, 43), (90, 48, 0, 89), (90, 102, 23, 17), (90, 102, 23, 61),
        (90, 48, 4, 53), (90, 48, 4, 79), (90, 72, 12, 41), (90, 72, 12, 67)
    ],
    49: [
        (90, 40, -1, 49), (90, 40, -1, 91), (90, 130, 46, 19), (90, 130, 46, 31),   #47, 7, 83
        (90, 76, 13, 37), (90, 76, 13, 67), (90, 94, 14, 13), (90, 94, 14, 73),
        (90, 140, 53, 11), (90, 140, 53, 29), (90, 86, 20, 47), 
        (90, 14, 0, 83), (90, 104, 27, 23), (90, 104, 27, 53),
        (90, 50, 0, 41), (90, 50, 0, 89), (90, 50, 6, 59), (90, 50, 6, 71),
        (90, 86, 10, 17), (90, 86, 10, 77), (90, 166, 76, 7), (90, 94, 24, 43), #43,43
        (90, 40, 3, 61), (90, 40, 3, 79)
    ],
    53: [
        (90, 36, -1, 53), (90, 36, -1, 91), (90, 144, 57, 17), (90, 144, 57, 19),
        (90, 54, 0, 37), (90, 54, 0, 89), (90, 36, 3, 71), (90, 36, 3, 73),
        (90, 156, 67, 11), (90, 156, 67, 13), (90, 84, 15, 29), (90, 84, 15, 67),
        (90, 84, 19, 47), (90, 84, 19, 49), (90, 66, 4, 31), (90, 66, 4, 83),
        (90, 96, 21, 23), (90, 96, 21, 61), (90, 96, 25, 41), (90, 96, 25, 43),
        (90, 114, 28, 7), (90, 114, 28, 59), (90, 24, 1, 77), (90, 24, 1, 79)
    ],
    59: [
        (90, 30, -1, 59), (90, 30, -1, 91), (90, 120, 38, 19), (90, 120, 38, 41),
        (90, 66, 7, 37), (90, 66, 7, 77), (90, 84, 12, 23), (90, 84, 12, 73),
        (90, 90, 9, 11), (90, 90, 9, 79), (90, 90, 19, 29), (90, 90, 19, 61),
        (90, 126, 39, 7), (90, 126, 39, 47), (90, 54, 3, 43), (90, 54, 3, 83),
        (90, 114, 31, 13), (90, 114, 31, 53), (90, 60, 0, 31), (90, 60, 0, 89),
        (90, 60, 8, 49), (90, 60, 8, 71), (90, 96, 18, 17), (90, 96, 18, 67)
    ],
    61: [
        (90, 28, -1, 61), (90, 28, -1, 91), (90, 82, 8, 19), (90, 82, 8, 79),
        (90, 100, 27, 37), (90, 100, 27, 43), (90, 100, 15, 7), (90, 100, 15, 73),
        (90, 98, 16, 11), (90, 98, 16, 71), (90, 62, 0, 29), (90, 62, 0, 89),
        (90, 80, 17, 47), (90, 80, 17, 53), (90, 80, 5, 17), (90, 80, 5, 83),
        (90, 100, 19, 13), (90, 100, 19, 67), (90, 118, 38, 31), 
        (90, 82, 18, 49), (90, 80, 9, 23), (90, 80, 9, 77), (90, 98, 26, 41), (90, 62, 10, 59) #59,59
    ],
    67: [
        (90, 22, -1, 67), (90, 22, -1, 91), (90, 148, 60, 13), (90, 148, 60, 19),
        (90, 112, 34, 31), (90, 112, 34, 37), (90, 58, 7, 49), (90, 58, 7, 73),
        (90, 122, 37, 11), (90, 122, 37, 47), (90, 68, 4, 29), (90, 68, 4, 83),
        (90, 122, 39, 17), (90, 122, 39, 41), (90, 68, 12, 53), (90, 68, 12, 59),
        (90, 32, 2, 71), (90, 32, 2, 77), (90, 112, 26, 7), (90, 112, 26, 61),
        (90, 58, 5, 43), (90, 58, 5, 79), (90, 68, 0, 23), (90, 68, 0, 89)
    ],
    71: [
        (90, 18, -1, 71), (90, 18, -1, 91), (90, 72, 0, 19), (90, 72, 0, 89),
        (90, 90, 21, 37), (90, 90, 21, 53), (90, 90, 13, 17), (90, 90, 13, 73),
        (90, 138, 51, 11), (90, 138, 51, 31), (90, 102, 27, 29), (90, 102, 27, 49),
        (90, 120, 36, 13), (90, 120, 36, 47), (90, 30, 1, 67), (90, 30, 1, 83),
        (90, 150, 61, 7), (90, 150, 61, 23), (90, 78, 15, 41), (90, 78, 15, 61),
        (90, 42, 3, 59), (90, 42, 3, 79), (90, 60, 6, 43), (90, 60, 6, 77)
    ],
    73: [
        (90, 16, -1, 73), (90, 16, -1, 91), (90, 124, 41, 19), (90, 124, 41, 37),
        (90, 146, 58, 11), (90, 146, 58, 23), (90, 74, 8, 29), (90, 74, 8, 77),
        (90, 74, 14, 47), (90, 74, 14, 59), (90, 56, 3, 41), (90, 56, 3, 83),
        (90, 106, 24, 13), (90, 106, 24, 61), (90, 106, 30, 31), (90, 106, 30, 43),
        (90, 124, 37, 7), (90, 124, 37, 49), (90, 34, 2, 67), (90, 34, 2, 79),
        (90, 74, 0, 17), (90, 74, 0, 89), (90, 56, 7, 53), (90, 56, 7, 71)
    ],
    77: [
        (90, 12, -1, 77), (90, 12, -1, 91), (90, 138, 52, 19), (90, 138, 52, 23),
        (90, 102, 28, 37), (90, 102, 28, 41), (90, 48, 5, 59), (90, 48, 5, 73),
        (90, 162, 72, 7), (90, 162, 72, 11), (90, 108, 31, 29), (90, 108, 31, 43),
        (90, 72, 13, 47), (90, 72, 13, 61), (90, 18, 0, 79), (90, 18, 0, 83),
        (90, 78, 0, 13), (90, 78, 0, 89), (90, 132, 47, 17), (90, 132, 47, 31),
        (90, 78, 16, 49), (90, 78, 16, 53), (90, 42, 4, 67), (90, 42, 4, 71)
    ],
    79: [
        (90, 10, -1, 79), (90, 10, -1, 91), (90, 100, 22, 19), (90, 100, 22, 61),
        (90, 136, 48, 7), (90, 136, 48, 37), (90, 64, 8, 43), (90, 64, 8, 73),
        (90, 80, 0, 11), (90, 80, 0, 89), (90, 80, 12, 29), (90, 80, 12, 71),
        (90, 116, 34, 17), (90, 116, 34, 47), (90, 44, 2, 53), (90, 44, 2, 83),
        (90, 154, 65, 13), (90, 100, 26, 31), (90, 100, 26, 49),
        (90, 46, 5, 67), (90, 134, 49, 23),  (90, 80, 16, 41), (90, 80, 16, 59), #41,59
        (90, 26, 1, 77) #77,77
        
    ],
    83: [
        (90, 6, -1, 83), (90, 6, -1, 91), (90, 114, 33, 19), (90, 114, 33, 47),
        (90, 114, 35, 29), (90, 114, 35, 37), (90, 96, 14, 11), (90, 96, 14, 73),
        (90, 126, 41, 13), (90, 126, 41, 41), (90, 126, 43, 23), (90, 126, 43, 31),
        (90, 54, 5, 49), (90, 54, 5, 77), (90, 54, 7, 59), (90, 54, 7, 67),
        (90, 84, 0, 7), (90, 84, 0, 89), (90, 66, 9, 43), (90, 66, 9, 71),
        (90, 66, 11, 53), (90, 66, 11, 61), (90, 84, 8, 17), (90, 84, 8, 79)
    ],
    89: [
        (90, 0, -1, 89), (90, 0, -1, 91), (90, 90, 14, 19), (90, 90, 14, 71),
        (90, 126, 42, 17), (90, 126, 42, 37), (90, 54, 6, 53), (90, 54, 6, 73),
        (90, 120, 35, 11), (90, 120, 35, 49), (90, 120, 39, 29), (90, 120, 39, 31),
        (90, 66, 10, 47), (90, 66, 10, 67), (90, 84, 5, 13), (90, 84, 5, 83),
        (90, 114, 34, 23), (90, 114, 34, 43), (90, 60, 5, 41), (90, 60, 5, 79),
        (90, 60, 9, 59), (90, 60, 9, 61), (90, 96, 11, 7), (90, 96, 11, 77)
    ],

    
    
    1: [
        (90, -2, 0, 91), (90, 142, 56, 19), (90, 70, 10, 37),
        (90, 128, 43, 11), (90, 92, 21, 29), (90, 110, 32, 23),
        (90, 20, 1, 77), (90, 160, 71, 7), (90, 88, 19, 31),
        (90, 52, 5, 49), (90, 70, 12, 43), (90, 110, 30, 17),
        (90, 38, 4, 71), (90, 2, 0, 89),
        
        (90, 70, 10, 73),
        (90, 128, 43, 41), (90, 92, 21, 59), (90, 110, 32, 47),
        (90, 20, 1, 83), (90, 160, 71, 13), (90, 88, 19, 61),
        (90, 52, 5, 79), (90, 70, 12, 67), (90, 110, 30, 53)
        
    ]
}
if __name__ == '__main__':
    print("Testing Total Primes and Largest Prime up to 1B")
    n_max = 333300001  # ~3.05B
    coprime_24 = [7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 49, 53, 59, 61, 67, 71, 73, 77, 79, 83, 89, 1]
    limit = 10**6  # Cap at 1B

    print(f"\nRunning on {cpu_count()} cores, processing n_max = {n_max} up to {limit}")
    amplitude = mark_composites(n_max, operators, coprime_24)
    total_primes, largest_prime = compute_primes_and_largest(n_max, amplitude, coprime_24, limit)

    total_with_235 = total_primes + 3  # Add 2, 3, 5
    expected_primes = 50847534  # π(10^9)
    print(f"Total Primes (24 classes up to 1B): {total_primes}")
    print(f"Total Primes (with 2, 3, 5): {total_with_235}")
    print(f"Expected Primes (π(10^9)): {expected_primes}")
    print(f"Difference (Total - Expected): {total_with_235 - expected_primes}")
    print("\nLargest Prime per Class:")
    for k in coprime_24:
        p = largest_prime[k]
        status = "Prime" if is_prime(p) else f"Composite (Factors: {factorize(p)})"
        print(f"k = {k}: Largest Prime = {p}: {status}")