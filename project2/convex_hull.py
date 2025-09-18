# Uncomment this line to import some functions that can help
# you debug your algorithm
import matplotlib.pyplot as plt
from plotting import draw_line, draw_hull, circle_point

def find_average_x(points: list[tuple[float, float]]) -> float:
    average_x = 0.0
    for tup in points:
        average_x += tup[0]
    average_x /= len(points)
    return average_x

def split_into_left_right(points: list[tuple[float, float]], left: list[tuple[float, float]], 
                            right: list[tuple[float, float]], 
                            avg_x: float) -> tuple[list[tuple[float, float]], list[tuple[float, float]]]:
    
    for tpl in points:
        if tpl[0] < avg_x:
            left.append(tpl)
        else:
            right.append(tpl)
        
    return (left, right)

def find_extreme_point(points: list[tuple[float, float]], find_right_most: bool) -> tuple[float, float]:
    
    if find_right_most:
        return max(points, key=lambda p: p[0])
    else:
        return min(points, key=lambda p: p[0])

def calculate_slope(left_point: tuple[float,float], right_point: tuple[float,float]) -> float:
    return (right_point[1] - left_point[1])/ (right_point[0] - left_point[0])
    
def is_bigger_tangent_line(temp: float, curr_slope: float) -> bool:
    return temp < curr_slope

def is_smaller_tangent_line(temp: float, curr_slope: float) -> bool:
    return temp > curr_slope 

def find_neighbor(points: list[tuple[float, float]], current_point: tuple[float, float],
                   isClockwise: bool) -> tuple[float, float]:
    idx = points.index(current_point)
    if isClockwise:
        return points[(idx - 1) % len(points)]
    else:
        return points[(idx + 1) % len(points)]

def find_upper_Tangent(left: list[tuple[float, float]], 
                       right: list[tuple[float, float]]) -> tuple[tuple[float, float], tuple[float, float]]:
    
    p: tuple[float, float] = find_extreme_point(left, True)
    q: tuple[float, float] = find_extreme_point(right, False)

    temp: float = calculate_slope(p, q)
    done: bool = False

    if len(left) == 1 and len(right) == 1:
        return (p, q)

    while not done:
        done = True  

        
        while True:
            r = find_neighbor(left, p, isClockwise=False)  
            if r == p:
                break  
            prev_slope = temp
            curr_slope = calculate_slope(r, q)

            if is_smaller_tangent_line(prev_slope, curr_slope):  
                temp = curr_slope
                p = r
                done = False
            else:
                break  

        
        while True:
            v = find_neighbor(right, q, isClockwise=True)
            if v == q:
                break  
            prev_slope = temp
            curr_slope = calculate_slope(v, p)

            if is_bigger_tangent_line(prev_slope, curr_slope):
                temp = curr_slope
                q = v
                done = False
            else:
                break

    return (p, q)


def find_Lower_Tangent(left: list[tuple[float, float]], 
                       right: list[tuple[float, float]]) -> tuple[tuple[float, float], tuple[float, float]]:

    p: tuple[float, float] = find_extreme_point(left, True)  
    q: tuple[float, float] = find_extreme_point(right, False)  
    temp: float = calculate_slope(p, q)
    done: bool = False

    while not done:
        done = True  

        
        while True:
            r = find_neighbor(left, p, isClockwise=True)  
            if r == p:
                break  
            prev_slope = temp
            curr_slope = calculate_slope(r, q)

            if is_bigger_tangent_line(prev_slope, curr_slope):  
                temp = curr_slope
                p = r
                done = False
            else:
                break  

        
        while True:
            v = find_neighbor(right, q, isClockwise=False)  
            if v == q:
                break  
            prev_slope = temp
            curr_slope = calculate_slope(v, p)

            if is_smaller_tangent_line(prev_slope, curr_slope):  
                temp = curr_slope
                q = v
                done = False
            else:
                break  

    return (p, q)

    
def combine(upper:list[tuple], lower:list[tuple], left:list[tuple[float, float]], 
            right:list[tuple[float, float]])-> list[tuple[float, float]]:
    
    combined_hull: list[tuple[float,float]] = []

    right_start = right.index(lower[1])
    right_stop = right.index(upper[1])

    left_start = left.index(upper[0])
    left_stop = left.index(lower[0])



    if len(right) == 1:
        combined_hull.append(right[0])
    else:
        current_idx = right_start
        while True:
    
            combined_hull.append(right[current_idx])

            if right[current_idx] == right[right_stop]:
                break

            current_idx = (current_idx + 1) % len(right)

    if len(left) == 1:
        combined_hull.append(left[0])
    else:
        current_idx = left_start
        while True:
    
            combined_hull.append(left[current_idx])

            if left[current_idx] == left[left_stop]:
                break

            current_idx = (current_idx + 1) % len(left)

    return combined_hull

def compute_hull_helper(points: list[tuple[float, float]]) -> list[tuple[float, float]]:
    theta = 2 #threshold value
    if len(points) <= theta:
        return points

    average_x = find_average_x(points)
    
    left:list[tuple[float, float]] = []
    right:list[tuple[float, float]] = []

    left, right = split_into_left_right(points, left, right, average_x)

    left_hull:list[tuple[float, float]] = compute_hull_helper(left)
    right_hull:list[tuple[float, float]] = compute_hull_helper(right)

    upper:list[tuple] = list(find_upper_Tangent(left_hull, right_hull))
    lower:list[tuple] = list(find_Lower_Tangent(left_hull, right_hull))

    convex_hull:list[tuple[float, float]] = combine(upper, lower, left_hull, right_hull)

    return convex_hull




def compute_hull(points: list[tuple[float, float]]) -> list[tuple[float, float]]:
    points.sort(key=lambda point: point[0])

    convex_hull = compute_hull_helper(points)

    draw_hull(convex_hull)
    plt.show()

    return convex_hull