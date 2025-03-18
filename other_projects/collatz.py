def collatz(n, so_far):
    so_far.append(n)
    if n == 1:
        print(' → '.join([str(m) for m in so_far]))
        # print(f'{so_far[0]} takes {len(so_far)} steps and reaches {max(so_far)}')
        return
    if n % 2 == 0:
        collatz(n // 2, so_far)
    else:
        collatz(3*n + 1, so_far)

collatz(871, [])

# for i in range(1, 100):
#     collatz(i, [])
