def tribonacci(n: int) -> int:
        
        sums:list[int] = []
        
        for i in range(n+1):
            if len(sums) == 0:
                sums.append(0)
            elif len(sums) == 1 or len(sums) == 2:
                sums.append(1)
            else:
                sums.append(sums[i-3] + sums[i-2] + sums[i-1])
        
        return sums[n]

print(tribonacci(4))
