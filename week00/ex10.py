def solution(N, M):
    day = 0
    while N > 0:
        day += 1
        N -= 1
        if day % M == 0:
            N += 1
    return day

# N = 3
# M = 5
# print(solution(N, M)