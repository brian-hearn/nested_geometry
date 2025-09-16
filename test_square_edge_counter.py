import math

def square_edge_counter(n: int, mode) -> int:
    if n < 0:
        raise ValueError("Input must be a natural number (>= 0).")
    
    k = math.isqrt(n) # largest square root ≤ n
    d = n - k*k
    
    if mode == 'square':
        base = (4*(k-2)**2 + 3*4*(k-2) + 2*4)/2
        if d == 0:
            j = 0
        elif 1 <= d <= k:
            j = 1 + 2*(d-1)
        elif k+1 <= d <= 2*k + 1:
            j = 2*(d-1)
        else:
            raise ValueError(f"Invalid d={d} for n={n}, k={k}")
    
    if mode == 'diagonals':
        base = (8*(k-2)**2 + 5*4*(k-2) + 3*4)/2
        extra_nodes = 0
        j = 0
        while d > 0:
            if extra_nodes == 0:
                j+= 3
            elif 1 <= extra_nodes <= k - 3:
                j+= 4
            elif extra_nodes == k - 2:
                j+= 3
            elif k - 1 <= extra_nodes <= 2*(k - 2) - 1:
                j+= 4
            elif extra_nodes == 2*k - 4:
                j+= 3
            elif extra_nodes == 2*k - 3:
                j+= 4
            elif 2*k - 2 <= extra_nodes <= 2*k:
                j+= 3
            d -= 1
            extra_nodes += 1
        # if d == 0:
        #     j = 0
        # elif 1 <= d <= k - 2:
        #     j = 3 + 4*(d-1)
        # elif k - 1 <= d <= 2*(k - 2):
        #     j = 6 + 4*(d-2)
        # elif 2*k - 3 <= d <= 2*k + 1:
        #     j = 6 + 4*(2*(k - 2)-2) + 
        # else:
        #     raise ValueError(f"Invalid d={d} for n={n}, k={k}")
        
        low_val_dict = {0: 0,
                        1: 0,
                        2: 1,
                        3: 3,
                        4: 6,
                        5: 8,
                        6: 11,
                        7: 14,
                        8: 17}
        
    
    return low_val_dict.get(n, int(base + j))

# for i in range(25,50):
#     print('----')
#     print(i)
#     print(square_edge_counter(i))

def even_division(n: int, s: int) -> list[int]:
    if s <= 0:
        raise ValueError("s must be a positive integer")
    base = n // s   # the smallest value each part gets
    remainder = n % s  # how many parts need +1
    result = [base + 1] * remainder + [base] * (s - remainder) # First 'remainder' parts get base+1, rest get base
    return result

def multiple_square_edge_counter(n: int, s: int, mode) -> int:
    part_sizes = even_division(n, s)
    count = 0
    for size in part_sizes:
        count += square_edge_counter(size, mode)
    max_val = max(part_sizes)
    min_val = min(part_sizes)
    if max_val != min_val:
        times_max = part_sizes.count(max_val)
        count += (s - 1)*min(part_sizes) + (times_max - 1)
    else:
        count += (s - 1)*min(part_sizes)
    return count

# for n in range(50):
#         print('Checking n = ' + str(n) + ' and s = ' + str(s) + '.')
#         print(multiple_square_edge_counter(n,s, mode = 'diagonals'))


# for n in range(10000):
#     for s in range(2,3):
#         print('Checking n = ' + str(n) + ' and s = ' + str(s) + '.')
#         print('One square has at most: ' + str(8*n))
#         print('Can find at least: ' + str(multiple_square_edge_counter(n,s, mode = 'diagonals')))


n = 500
s = 3
for n in range(300):
    print('Checking n = ' + str(n) + ' and s = ' + str(s) + '.')
    print('A \'weakly connected\' solution has at most ' + str(4*n) + ' edges.')
    result = multiple_square_edge_counter(n,s, mode = 'diagonals')
    print('But there exists a solution with ' + str(4*n) + ' edges!')
    if result > 4*n:
        print('!!!')

