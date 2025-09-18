import math
import random
import copy
import heapq

from tsp_core import Tour, SolutionStats, Timer, score_tour, Solver
from tsp_cuttree import CutTree
from math import inf

class Node:

    def __init__(self, path: list[int], visited: set, 
                 reduced_matrix: list[list[float]], lower_bound: float, remaining: int) -> None:
        self.path = path
        self.visited = visited
        self.lower_bound = lower_bound
        self.reduced_matrix = reduced_matrix
        self.remaining = remaining

def random_tour(edges: list[list[float]], timer: Timer) -> list[SolutionStats]:
    stats = []
    n_nodes_expanded = 0
    n_nodes_pruned = 0
    cut_tree = CutTree(len(edges))

    while True:
        if timer.time_out():
            return stats

        tour = random.sample(list(range(len(edges))), len(edges))
        n_nodes_expanded += 1

        cost = score_tour(tour, edges)
        if math.isinf(cost):
            n_nodes_pruned += 1
            cut_tree.cut(tour)
            continue

        if stats and cost > stats[-1].score:
            n_nodes_pruned += 1
            cut_tree.cut(tour)
            continue

        stats.append(SolutionStats(
            tour=tour,
            score=cost,
            time=timer.time(),
            max_queue_size=1,
            n_nodes_expanded=n_nodes_expanded,
            n_nodes_pruned=n_nodes_pruned,
            n_leaves_covered=cut_tree.n_leaves_cut(),
            fraction_leaves_covered=cut_tree.fraction_leaves_covered()
        ))

    if not stats:
        return [SolutionStats(
            [],
            math.inf,
            timer.time(),
            1,
            n_nodes_expanded,
            n_nodes_pruned,
            cut_tree.n_leaves_cut(),
            cut_tree.fraction_leaves_covered()
        )]

def greedy_tour(edges: list[list[float]], timer: Timer) -> list[SolutionStats]:
    stats:list[SolutionStats] = []
    cut_tree = CutTree(len(edges))
    n = len(edges)
    
    while not timer.time_out():
        for city in range(n):
            if timer.time_out():
                break
            
            tour:list[int] = [city]
            visited:set = set(tour)
            current_city:int = city
            total_cost:float = 0.0
            dead_end:bool = False

            while len(visited) < n:
                next_neighbor:int|None = None
                min_cost:float  = float('inf')
                for neighbor in range(n):
                    if neighbor not in visited and edges[current_city][neighbor] < min_cost:
                        next_neighbor = neighbor
                        min_cost = edges[current_city][neighbor]
                
                if next_neighbor is None and not math.isfinite(min_cost):
                        dead_end = True
                        break

                tour.append(next_neighbor)
                visited.add(next_neighbor)
                total_cost += min_cost
                current_city = next_neighbor
            
            if not dead_end:
                total_cost += edges[current_city][city]

                stats.append(SolutionStats(tour = tour, 
                                        score = total_cost, 
                                        time = timer.time(), 
                                        max_queue_size=1, 
                                        n_nodes_expanded=len(tour), 
                                        n_nodes_pruned = 0, 
                                        n_leaves_covered=cut_tree.n_leaves_cut(), 
                                        fraction_leaves_covered=cut_tree.fraction_leaves_covered()))

                return stats
        
    return stats

def dfs(edges: list[list[float]], timer: Timer) -> list[SolutionStats]:
    stats: list[SolutionStats] = []
    n = len(edges)
    cut_tree: CutTree = CutTree(n)
    stack: list[tuple[list[int], set[int]]] = [([0], {0})]  
    bssf_score: float = math.inf
    max_queue: int = 1
    n_expanded: int = 0

    while stack and not timer.time_out():
        current_path, visited = stack.pop()
        n_expanded += 1

        if len(current_path) == n:
            tour = current_path
            score = score_tour(tour + [tour[0]], edges)  

            if not math.isinf(score) and score < bssf_score:
                stats.append(SolutionStats(
                    tour=tour,
                    score=score,
                    time=timer.time(),
                    max_queue_size=max_queue,
                    n_nodes_expanded=n_expanded,
                    n_nodes_pruned=0,
                    n_leaves_covered=cut_tree.n_leaves_cut(),
                    fraction_leaves_covered=cut_tree.fraction_leaves_covered()
                ))
                bssf_score = score
        else:
            current_city = current_path[-1]
            for child_city in range(n):
                if child_city not in visited and not math.isinf(edges[current_city][child_city]):

                    new_path = current_path + [child_city]
                    new_visited = visited | {child_city}
                    stack.append((new_path, new_visited))
            
            max_queue = max(max_queue, len(stack))

    return stats 

def branch_and_bound(edges: list[list[float]], timer: Timer) -> list[SolutionStats]:
    # set the diagonal to inf before reducing matrices
    for i in range(len(edges)): 
        edges[i][i] = inf  


    inital_answer:list[SolutionStats] = greedy_tour(edges, timer)
    bssf:float = inital_answer[0].score
    reduced_matrix, lower_bound = reduce_matrix(edges, [])
    stats: list[SolutionStats] = []
    n = len(edges)
    cut_tree: CutTree = CutTree(n)

    initial_path = [0]
    initial_visited = {0}
    stack: list[tuple[list[int], set[int], list[list[float]], float]] = [(initial_path, initial_visited, reduced_matrix, lower_bound)]  
    
    max_queue: int = 1
    n_expanded: int = 0
    n_pruned: int = 0

    while stack and not timer.time_out():
        current_path, visited, current_edges, current_lbound = stack.pop()
        n_expanded += 1

        if len(current_path) == n:
            tour = current_path
            score = score_tour(tour, edges)  

            if not math.isinf(score) and score < bssf:
                stats.append(SolutionStats(
                    tour=tour,
                    score=score,
                    time=timer.time(),
                    max_queue_size=max_queue,
                    n_nodes_expanded=n_expanded,
                    n_nodes_pruned= n_pruned,
                    n_leaves_covered=cut_tree.n_leaves_cut(),
                    fraction_leaves_covered=cut_tree.fraction_leaves_covered()
                ))
                bssf = score
        else:
            current_city = current_path[-1]

            for child_city in range(n):
                if child_city not in visited and not math.isinf(edges[current_city][child_city]):
                    
                    new_edges = copy.deepcopy(current_edges)
                    
                    for j in range(n):
                        new_edges[current_city][j] = inf
                        
                    for i in range(n):
                        new_edges[i][child_city] = inf
                    
                    if len(visited) == n-1:
                        new_edges[child_city][0] = inf
                    
                    new_edges, additional_cost = reduce_matrix(new_edges, current_path)

                    if additional_cost != inf:
                    
                        new_bound = current_lbound + current_edges[current_city][child_city] + additional_cost
                        
                        if new_bound < bssf:
                            new_path = current_path + [child_city]
                            new_visited = visited | {child_city}
                            stack.append((new_path, new_visited, new_edges, new_bound))
                        else:
                            n_pruned += 1
                            cut_tree.cut(current_path + [child_city])

                    else:
                        n_pruned += 1
                        cut_tree.cut(current_path + [child_city])
            
            max_queue = max(max_queue, len(stack))
    
    if stats == []:
        return inital_answer
    
    return stats 

def branch_and_bound_smart(edges: list[list[float]], timer: Timer) -> list[SolutionStats]:
    for i in range(len(edges)): 
        edges[i][i] = inf  

    inital_answer:list[SolutionStats] = greedy_tour(edges, timer)
    bssf = inital_answer[0].score
    reduced_matrix, lower_bound = reduce_matrix(edges, [])

    stats: list[SolutionStats] = []
    n = len(edges)
    cut_tree: CutTree = CutTree(n)

    initial_path:list = [0]
    initial_visited:set = {0}

    priority_queue: list = []

    counter:int = 0
    initial_node: Node = Node(initial_path, initial_visited, reduced_matrix, lower_bound, n-1)
    heapq.heappush(priority_queue, (calculate_priority(initial_node), 0, initial_node))
    counter += 1

    max_queue: int = 1
    n_expanded: int = 0
    n_pruned: int = 0

    while priority_queue and not timer.time_out():

        current_node:Node = heapq.heappop(priority_queue)[2]  
        current_path = current_node.path
        n_expanded += 1

        if current_node.lower_bound >= bssf:
            continue

        if len(current_path) == n:
            tour = current_path
            score = score_tour(tour, edges)  

            if not math.isinf(score) and score < bssf:
                print(f'New score found: {score}')
                stats.append(SolutionStats(
                    tour=tour,
                    score=score,
                    time=timer.time(),
                    max_queue_size=max_queue,
                    n_nodes_expanded=n_expanded,
                    n_nodes_pruned= n_pruned,
                    n_leaves_covered=cut_tree.n_leaves_cut(),
                    fraction_leaves_covered=cut_tree.fraction_leaves_covered()
                ))
                bssf = score
        else:
            current_city = current_path[-1]

            for child_city in range(n):
                if  (child_city not in current_node.visited) and current_node.reduced_matrix[current_city][child_city] != inf:
                    
                    new_edges = copy.deepcopy(current_node.reduced_matrix)
                    
                    for j in range(n):
                        new_edges[current_city][j] = inf
                        
                    for i in range(n):
                        new_edges[i][child_city] = inf
                    
                    if current_node.remaining == 1:
                        for k in range(n):
                            if k != 0:
                                new_edges[child_city][k] = inf
                        new_edges[child_city][0] = edges[child_city][0]
                    
                    new_edges, additional_cost = reduce_matrix(new_edges, current_node.path)

                    if additional_cost != inf:
                    
                        new_bound = current_node.lower_bound + current_node.reduced_matrix[current_city][child_city] + additional_cost
                        
                        if new_bound < bssf:
                            child_visited:set[int] = current_node.visited.copy()
                            child_visited.add(child_city)
                            child_path:list[int] = current_node.path + [child_city]
                            
                            child_node = Node(child_path, 
                                                child_visited,
                                                new_edges,
                                                new_bound,
                                                current_node.remaining - 1)
                            heapq.heappush(priority_queue, (calculate_priority(child_node), counter, child_node))
                            counter += 1

                        else:
                            n_pruned += 1
                            cut_tree.cut(current_path + [child_city])

                    else:
                        n_pruned += 1
                        cut_tree.cut(current_path + [child_city])

            max_queue = max(max_queue, len(priority_queue))

    if stats == inf:
        return inital_answer
    
    return stats

def reduce_matrix(matrix: list[list[float]], path: list[int]) -> tuple[list[list[float]], float]:
    n = len(matrix)
    matrix_copy = copy.deepcopy(matrix)
    lower_bound = 0.0

    for row in range(n):
        if len(path) != 0 and row in path[:-1]:
            continue

        finite_values = [val for val in matrix_copy[row] if val != math.inf]
        if finite_values:
            row_min = min(finite_values)
            lower_bound += row_min
            for col in range(n):
                if matrix_copy[row][col] != math.inf:
                    matrix_copy[row][col] -= row_min

    for col in range(n):
        if len(path) != 0 and col in path[1:]:
            continue

        finite_values = [matrix_copy[row][col] for row in range(n) if matrix_copy[row][col] != math.inf]
        if finite_values:
            col_min = min(finite_values)
            lower_bound += col_min
            for row in range(n):
                if matrix_copy[row][col] != math.inf:
                    matrix_copy[row][col] -= col_min

    return matrix_copy, lower_bound

def calculate_priority(node: Node) -> float:
    if math.isinf(node.lower_bound):
        return inf
    return (node.lower_bound * 10000) - (len(node.path)*500)
