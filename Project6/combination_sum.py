def combinationSum(candidates, target):
    result = []
    divide_and_conquer(0, target, [], candidates, result)
    return result

def divide_and_conquer(start, target, path:list, candidates, result:list):
        
        if target == 0:
            result.append(path[:])
            return
        
        for i in range(start, len(candidates)):
            
            if candidates[i] > target:
                continue
            
            path.append(candidates[i])
            divide_and_conquer(i, target - candidates[i], path, candidates, result)
            
            path.pop()


candidates = [7,2,3]

target = 7

print(combinationSum(candidates, target))