def findCircleNum(isConnected: list[list[int]]) -> int:

    def dfs(city:int)->None:
        for neighbor in range(len(isConnected)):

            if isConnected[city][neighbor] == 1 and neighbor not in visited:
                
                visited.add(neighbor)
                dfs(neighbor)

    visited:set = set()
    ans:int = 0

    for city in range(len(isConnected)):
        if city not in visited:
            ans +=1 
            visited.add(city)
            dfs(city)

    return ans

isconnected = [[1,1,0],[1,1,0],[0,0,1]]

print(findCircleNum(isconnected))